#pragma once
#include <string>
#include <vector>
#include <sstream>
#include <iomanip>
#include <stdexcept>
#include <bitset>
#include <cstdint>

// ─── Hex formatting helpers ───────────────────────────────────────────────────
inline std::string to_hex8(uint8_t v) {
    std::ostringstream ss;
    ss << "0x" << std::uppercase << std::hex
       << std::setw(2) << std::setfill('0') << static_cast<int>(v);
    return ss.str();
}
inline std::string to_hex16(uint16_t v) {
    std::ostringstream ss;
    ss << "0x" << std::uppercase << std::hex
       << std::setw(4) << std::setfill('0') << static_cast<int>(v);
    return ss.str();
}

inline void validate_bit_string(const std::string& bits, const std::string& label) {
    if (bits.empty()) throw std::invalid_argument(label + ": data must not be empty");
    for (char ch : bits) {
        if (ch != '0' && ch != '1')
            throw std::invalid_argument(label + ": input must contain only 0 and 1");
    }
}

inline std::string pack_bits_to_bytes(const std::string& bits) {
    std::string out((bits.size() + 7) / 8, '\0');
    for (size_t i = 0; i < bits.size(); i++) {
        if (bits[i] == '1') {
            size_t byte_idx = i / 8;
            int bit_pos = 7 - static_cast<int>(i % 8);
            out[byte_idx] = static_cast<char>(static_cast<uint8_t>(out[byte_idx]) | (1u << bit_pos));
        }
    }
    return out;
}

inline std::string unpack_bytes_to_bits(const std::string& bytes, size_t bit_len) {
    std::string bits;
    bits.reserve(bit_len);
    for (size_t i = 0; i < bit_len; i++) {
        size_t byte_idx = i / 8;
        int bit_pos = 7 - static_cast<int>(i % 8);
        uint8_t b = static_cast<uint8_t>(bytes[byte_idx]);
        bits.push_back((b & (1u << bit_pos)) ? '1' : '0');
    }
    return bits;
}

// =========================================================================
//  1. PARITY  (even parity over entire bit string)
//
//  Rule: parity bit = (number_of_1_bits % 2)
//        so that total ones including parity bit is even.
//
//  Wire layout : [1 byte: bit_len] [bit chars '0'/'1'] [1 byte parity bit (0/1)]
//  Socket tag  : "PR|"
// =========================================================================
struct ParityResult {
    std::string bits;
    uint8_t     parity_bit;
    int         ones_count;
    bool        ok;
};

inline ParityResult parity_encode(const std::string& bits) {
    validate_bit_string(bits, "Parity");
    if (bits.size() > 255)
        throw std::invalid_argument("Parity: max bit length is 255 for this packet format");

    ParityResult r;
    r.bits = bits;
    r.ones_count = 0;
    for (char b : bits) {
        if (b == '1') r.ones_count++;
    }
    r.parity_bit = static_cast<uint8_t>(r.ones_count % 2);
    r.ok = true;
    return r;
}

inline std::string parity_pack(const ParityResult& r) {
    std::string out;
    out += static_cast<char>(r.bits.size());
    out += r.bits;
    out += static_cast<char>(r.parity_bit);
    return out;
}

inline ParityResult parity_decode(const std::string& wire) {
    if (wire.size() < 2) throw std::runtime_error("Parity: packet too short");
    size_t bit_len = static_cast<uint8_t>(wire[0]);
    if (wire.size() < 1 + bit_len + 1)
        throw std::runtime_error("Parity: truncated packet");
    std::string bits = wire.substr(1, bit_len);
    uint8_t recv_parity = static_cast<uint8_t>(wire[1 + bit_len]);
    if (recv_parity > 1)
        throw std::runtime_error("Parity: invalid parity bit in packet");

    ParityResult r = parity_encode(bits);
    r.ok = (r.parity_bit == recv_parity);
    return r;
}

// =========================================================================
//  2. BLOCK (2D) PARITY
//
//  Data bits are laid out row-major in a rows x cols matrix.
//  Row parity bit = XOR of bits in each row.
//  Col parity bit = XOR of bits in each column.
//
//  Wire layout : [1 byte: rows] [1 byte: cols] [rows*cols bit chars '0'/'1']
//                [row parity bits as bytes (rows)] [col parity bits as bytes (cols)]
//  Socket tag  : "BP|"
// =========================================================================
struct BlockParityResult {
    std::string                       bits;
    int                               rows, cols;
    std::vector<std::vector<uint8_t>> grid;
    std::vector<uint8_t>              row_parity;
    std::vector<uint8_t>              col_parity;
    bool                              ok;
};

inline BlockParityResult block_parity_encode(const std::string& bits, int rows, int cols) {
    if (rows <= 0 || cols <= 0)
        throw std::invalid_argument("Block parity: rows and cols must be > 0");
    if (rows > 255 || cols > 255)
        throw std::invalid_argument("Block parity: rows and cols must be <= 255");

    validate_bit_string(bits, "Block parity");
    if (static_cast<int>(bits.size()) != rows * cols)
        throw std::invalid_argument("Block parity: bit length must be exactly rows*cols");

    BlockParityResult r;
    r.bits = bits;
    r.rows = rows;
    r.cols = cols;
    r.ok   = true;
    r.col_parity.resize(cols, 0);

    for (int row = 0; row < r.rows; row++) {
        std::vector<uint8_t> rv;
        uint8_t rp = 0;
        for (int col = 0; col < cols; col++) {
            int idx = row * cols + col;
            uint8_t bit = static_cast<uint8_t>(bits[idx] - '0');
            rv.push_back(bit);
            rp ^= bit;
            r.col_parity[col] ^= bit;
        }
        r.grid.push_back(rv);
        r.row_parity.push_back(rp);
    }
    return r;
}

inline std::string block_parity_pack(const BlockParityResult& r) {
    std::string out;
    out += static_cast<char>(r.rows);
    out += static_cast<char>(r.cols);
    out += r.bits;
    for (uint8_t b : r.row_parity) out += static_cast<char>(b);
    for (uint8_t b : r.col_parity) out += static_cast<char>(b);
    return out;
}

inline BlockParityResult block_parity_decode(const std::string& wire) {
    if (wire.size() < 2) throw std::runtime_error("Block parity: packet too short");
    int rows = static_cast<uint8_t>(wire[0]);
    int cols = static_cast<uint8_t>(wire[1]);
    if (rows <= 0 || cols <= 0)
        throw std::runtime_error("Block parity: invalid rows/cols in packet");

    int data_len = rows * cols;
    if (static_cast<int>(wire.size()) < 2 + data_len + rows + cols)
        throw std::runtime_error("Block parity: truncated packet");

    std::string bits = wire.substr(2, data_len);
    validate_bit_string(bits, "Block parity");

    std::vector<uint8_t> recv_row(rows), recv_col(cols);
    int base = 2 + data_len;
    for (int i = 0; i < rows; i++) recv_row[i] = static_cast<uint8_t>(wire[base + i]);
    for (int i = 0; i < cols; i++) recv_col[i] = static_cast<uint8_t>(wire[base + rows + i]);

    for (int i = 0; i < rows; i++) {
        if (recv_row[i] > 1)
            throw std::runtime_error("Block parity: invalid row parity bit in packet");
    }
    for (int i = 0; i < cols; i++) {
        if (recv_col[i] > 1)
            throw std::runtime_error("Block parity: invalid col parity bit in packet");
    }

    BlockParityResult r = block_parity_encode(bits, rows, cols);
    r.ok = (r.row_parity == recv_row) && (r.col_parity == recv_col);
    return r;
}

// =========================================================================
//  3. CRC-8  (polynomial 0x07, CRC-8/SMBUS)
//
//  CRC starts at 0x00. For each byte: XOR into CRC, then process 8 bits:
//    if high bit set  -> shift left, XOR with 0x07
//    else             -> shift left
//  Append the 1-byte result after the data.
//
//  Input bits are packed MSB-first into bytes; last byte is right-padded with 0s.
//
//  Wire layout : [2 bytes: bit_len] [packed data bytes] [1 CRC byte]
//  Socket tag  : "CR|"
// =========================================================================
static const uint8_t CRC8_POLY = 0x07;

inline uint8_t crc8_compute(const std::string& data) {
    uint8_t crc = 0x00;
    for (unsigned char byte : data) {
        crc ^= byte;
        for (int i = 0; i < 8; i++) {
            if (crc & 0x80)
                crc = static_cast<uint8_t>((crc << 1) ^ CRC8_POLY);
            else
                crc = static_cast<uint8_t>(crc << 1);
        }
    }
    return crc;
}

struct CRC8Result {
    std::string bits;
    std::string packed_bytes;
    uint8_t     crc;
    bool        ok;
};

inline CRC8Result crc8_encode(const std::string& bits) {
    validate_bit_string(bits, "CRC-8");
    if (bits.size() > 65535)
        throw std::invalid_argument("CRC-8: max bit length is 65535 for this packet format");

    CRC8Result r;
    r.bits = bits;
    r.packed_bytes = pack_bits_to_bytes(bits);
    r.crc  = crc8_compute(r.packed_bytes);
    r.ok   = true;
    return r;
}

inline std::string crc8_pack(const CRC8Result& r) {
    std::string out;
    uint16_t bit_len = static_cast<uint16_t>(r.bits.size());
    out += static_cast<char>((bit_len >> 8) & 0xFF);
    out += static_cast<char>(bit_len & 0xFF);
    out += r.packed_bytes;
    out += static_cast<char>(r.crc);
    return out;
}

inline CRC8Result crc8_decode(const std::string& wire) {
    if (wire.size() < 4) throw std::runtime_error("CRC-8: packet too short");
    uint16_t bit_len = (static_cast<uint8_t>(wire[0]) << 8)
                     |  static_cast<uint8_t>(wire[1]);
    if (bit_len == 0)
        throw std::runtime_error("CRC-8: invalid bit length in packet");

    size_t data_len = (bit_len + 7) / 8;
    if (wire.size() < 2 + data_len + 1)
        throw std::runtime_error("CRC-8: truncated packet");

    std::string packed = wire.substr(2, data_len);
    uint8_t recv_crc = static_cast<uint8_t>(wire.back());
    CRC8Result r = crc8_encode(unpack_bytes_to_bits(packed, bit_len));
    r.ok = (r.crc == recv_crc);
    return r;
}

// =========================================================================
//  4. CHECKSUM  (16-bit one's complement, same as Internet checksum)
//
//  Data is treated as 16-bit big-endian words; odd-length data is zero-padded.
//  Sum all words with one's complement addition (carry wraps around).
//  Checksum = bitwise NOT of the sum.
//  Verification: sum of all words INCLUDING the checksum word == 0xFFFF.
//
//  Input bits are packed MSB-first into bytes; last byte is right-padded with 0s.
//
//  Wire layout : [2 bytes: bit_len] [packed data bytes] [2 checksum bytes, big-endian]
//  Socket tag  : "CS|"
// =========================================================================
inline uint16_t checksum_compute(const std::string& data) {
    uint32_t sum = 0;
    int len = static_cast<int>(data.size());
    for (int i = 0; i + 1 < len; i += 2) {
        uint16_t word = (static_cast<uint8_t>(data[i]) << 8)
                      |  static_cast<uint8_t>(data[i + 1]);
        sum += word;
    }
    if (len % 2 != 0)
        sum += (static_cast<uint8_t>(data[len - 1]) << 8);
    while (sum >> 16)
        sum = (sum & 0xFFFF) + (sum >> 16);
    return static_cast<uint16_t>(~sum);
}

struct ChecksumResult {
    std::string bits;
    std::string packed_bytes;
    uint16_t    checksum;
    bool        ok;
};

inline ChecksumResult checksum_encode(const std::string& bits) {
    validate_bit_string(bits, "Checksum");
    if (bits.size() > 65535)
        throw std::invalid_argument("Checksum: max bit length is 65535 for this packet format");

    ChecksumResult r;
    r.bits = bits;
    r.packed_bytes = pack_bits_to_bytes(bits);
    r.checksum = checksum_compute(r.packed_bytes);
    r.ok       = true;
    return r;
}

inline std::string checksum_pack(const ChecksumResult& r) {
    std::string out;
    uint16_t bit_len = static_cast<uint16_t>(r.bits.size());
    out += static_cast<char>((bit_len >> 8) & 0xFF);
    out += static_cast<char>(bit_len & 0xFF);
    out += r.packed_bytes;
    out += static_cast<char>((r.checksum >> 8) & 0xFF);
    out += static_cast<char>( r.checksum        & 0xFF);
    return out;
}

inline ChecksumResult checksum_decode(const std::string& wire) {
    if (wire.size() < 5) throw std::runtime_error("Checksum: packet too short");
    uint16_t bit_len = (static_cast<uint8_t>(wire[0]) << 8)
                     |  static_cast<uint8_t>(wire[1]);
    if (bit_len == 0)
        throw std::runtime_error("Checksum: invalid bit length in packet");

    size_t data_len = (bit_len + 7) / 8;
    if (wire.size() < 2 + data_len + 2)
        throw std::runtime_error("Checksum: truncated packet");

    std::string packed = wire.substr(2, data_len);
    uint16_t recv_cs = (static_cast<uint8_t>(wire[2 + data_len]) << 8)
                     |  static_cast<uint8_t>(wire[2 + data_len + 1]);

    ChecksumResult r = checksum_encode(unpack_bytes_to_bits(packed, bit_len));
    r.ok = (r.checksum == recv_cs);
    return r;
}
