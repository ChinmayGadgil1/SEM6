#pragma once
#include <string>
#include <vector>
#include <sstream>
#include <iomanip>
#include <stdexcept>
#include <bitset>
#include <cstdint>
#include <array>
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
inline std::vector<std::string> split_fields(const std::string& s, char delim) {
    std::vector<std::string> out;
    std::string cur;
    for (char c : s) {
        if (c == delim) {
            out.push_back(cur);
            cur.clear();
        } else {
            cur.push_back(c);
        }
    }
    out.push_back(cur);
    return out;
}
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
inline bool is_binary_bits(const std::string& s) {
    if (s.empty()) return false;
    for (char c : s)
        if (c != '0' && c != '1')
            return false;
    return true;
}

inline std::string crc_poly_remainder(const std::string& data_bits,
                                      const std::string& generator_bits) {
    if (!is_binary_bits(data_bits) || !is_binary_bits(generator_bits))
        throw std::invalid_argument("CRC: data and generator must be binary strings");
    if (generator_bits.size() < 2 || generator_bits.front() != '1' ||
        generator_bits.back() != '1') {
        throw std::invalid_argument("CRC: generator must start/end with 1 and length >= 2");
    }

    std::string work = data_bits + std::string(generator_bits.size() - 1, '0');
    for (size_t i = 0; i + generator_bits.size() <= work.size(); ++i) {
        if (work[i] == '1') {
            for (size_t j = 0; j < generator_bits.size(); ++j)
                work[i + j] = (work[i + j] == generator_bits[j]) ? '0' : '1';
        }
    }
    return work.substr(work.size() - (generator_bits.size() - 1));
}

inline bool crc_poly_verify(const std::string& transmitted_bits,
                            const std::string& generator_bits) {
    if (!is_binary_bits(transmitted_bits) || !is_binary_bits(generator_bits))
        throw std::invalid_argument("CRC verify: transmitted bits and generator must be binary strings");
    if (generator_bits.size() < 2 || generator_bits.front() != '1' ||
        generator_bits.back() != '1') {
        throw std::invalid_argument("CRC verify: generator must start/end with 1 and length >= 2");
    }
    if (transmitted_bits.size() < generator_bits.size() - 1)
        throw std::invalid_argument("CRC verify: transmitted bits too short");

    std::string work = transmitted_bits;
    for (size_t i = 0; i + generator_bits.size() <= work.size(); ++i) {
        if (work[i] == '1') {
            for (size_t j = 0; j < generator_bits.size(); ++j)
                work[i + j] = (work[i + j] == generator_bits[j]) ? '0' : '1';
        }
    }

    size_t rem_start = work.size() - (generator_bits.size() - 1);
    for (size_t i = rem_start; i < work.size(); ++i) {
        if (work[i] != '0') return false;
    }
    return true;
}

struct CRCPolyResult {
    std::string data_bits;
    std::string generator_bits;
    std::string remainder_bits;
    std::string transmitted_bits;
    bool        ok;
};

inline CRCPolyResult crc_poly_encode(const std::string& data_bits,
                                     const std::string& generator_bits) {
    CRCPolyResult r;
    r.data_bits = data_bits;
    r.generator_bits = generator_bits;
    r.remainder_bits = crc_poly_remainder(data_bits, generator_bits);
    r.transmitted_bits = data_bits + r.remainder_bits;
    r.ok = true;
    return r;
}

inline std::string crc_poly_pack(const CRCPolyResult& r) {
    return r.data_bits + "|" + r.generator_bits + "|" +
           r.remainder_bits + "|" + r.transmitted_bits;
}

inline CRCPolyResult crc_poly_decode(const std::string& wire) {
    auto parts = split_fields(wire, '|');
    if (parts.size() != 4)
        throw std::runtime_error("CRC: invalid packet format");

    CRCPolyResult r;
    r.data_bits = parts[0];
    r.generator_bits = parts[1];
    r.remainder_bits = parts[2];
    r.transmitted_bits = parts[3];

    std::string expected_rem = crc_poly_remainder(r.data_bits, r.generator_bits);
    std::string expected_tx = r.data_bits + expected_rem;
    r.ok = (r.remainder_bits == expected_rem) &&
           (r.transmitted_bits == expected_tx) &&
           crc_poly_verify(r.transmitted_bits, r.generator_bits);
    return r;
}
struct HammingResult {
    std::string data_bits;
    std::string encoded_bits;
    std::string decoded_bits;
    size_t      original_len;
    int         corrected_blocks;
    bool        ok;
};

inline HammingResult hamming_encode(const std::string& bits) {
    validate_bit_string(bits, "Hamming");

    HammingResult r;
    r.data_bits = bits;
    r.original_len = bits.size();
    r.corrected_blocks = 0;
    r.ok = true;

    std::string padded = bits;
    while (padded.size() % 4 != 0) padded.push_back('0');

    std::string enc;
    enc.reserve((padded.size() / 4) * 7);

    for (size_t i = 0; i < padded.size(); i += 4) {
        uint8_t d1 = static_cast<uint8_t>(padded[i] - '0');
        uint8_t d2 = static_cast<uint8_t>(padded[i + 1] - '0');
        uint8_t d3 = static_cast<uint8_t>(padded[i + 2] - '0');
        uint8_t d4 = static_cast<uint8_t>(padded[i + 3] - '0');

        uint8_t p1 = d1 ^ d2 ^ d4;
        uint8_t p2 = d1 ^ d3 ^ d4;
        uint8_t p4 = d2 ^ d3 ^ d4;

        enc.push_back(static_cast<char>('0' + p1));
        enc.push_back(static_cast<char>('0' + p2));
        enc.push_back(static_cast<char>('0' + d1));
        enc.push_back(static_cast<char>('0' + p4));
        enc.push_back(static_cast<char>('0' + d2));
        enc.push_back(static_cast<char>('0' + d3));
        enc.push_back(static_cast<char>('0' + d4));
    }

    r.encoded_bits = enc;
    r.decoded_bits = bits;
    return r;
}

inline std::string hamming_pack(const HammingResult& r) {
    return std::to_string(r.original_len) + "|" + r.encoded_bits;
}

inline HammingResult hamming_decode(const std::string& wire) {
    auto parts = split_fields(wire, '|');
    if (parts.size() != 2)
        throw std::runtime_error("Hamming: invalid packet format");

    size_t original_len = 0;
    try {
        original_len = static_cast<size_t>(std::stoul(parts[0]));
    } catch (...) {
        throw std::runtime_error("Hamming: invalid original length in packet");
    }

    std::string enc = parts[1];
    validate_bit_string(enc, "Hamming");
    if (enc.size() % 7 != 0)
        throw std::runtime_error("Hamming: encoded length must be a multiple of 7");

    int corrected = 0;
    std::string dec;
    dec.reserve((enc.size() / 7) * 4);

    for (size_t i = 0; i < enc.size(); i += 7) {
        uint8_t b1 = static_cast<uint8_t>(enc[i] - '0');
        uint8_t b2 = static_cast<uint8_t>(enc[i + 1] - '0');
        uint8_t b3 = static_cast<uint8_t>(enc[i + 2] - '0');
        uint8_t b4 = static_cast<uint8_t>(enc[i + 3] - '0');
        uint8_t b5 = static_cast<uint8_t>(enc[i + 4] - '0');
        uint8_t b6 = static_cast<uint8_t>(enc[i + 5] - '0');
        uint8_t b7 = static_cast<uint8_t>(enc[i + 6] - '0');

        uint8_t s1 = b1 ^ b3 ^ b5 ^ b7;
        uint8_t s2 = b2 ^ b3 ^ b6 ^ b7;
        uint8_t s4 = b4 ^ b5 ^ b6 ^ b7;
        uint8_t err_pos = static_cast<uint8_t>(s1 + (s2 << 1) + (s4 << 2));

        if (err_pos >= 1 && err_pos <= 7) {
            ++corrected;
            switch (err_pos) {
                case 1: b1 ^= 1; break;
                case 2: b2 ^= 1; break;
                case 3: b3 ^= 1; break;
                case 4: b4 ^= 1; break;
                case 5: b5 ^= 1; break;
                case 6: b6 ^= 1; break;
                case 7: b7 ^= 1; break;
            }
        }

        dec.push_back(static_cast<char>('0' + b3));
        dec.push_back(static_cast<char>('0' + b5));
        dec.push_back(static_cast<char>('0' + b6));
        dec.push_back(static_cast<char>('0' + b7));
    }

    if (original_len > dec.size())
        throw std::runtime_error("Hamming: original length exceeds decoded length");

    HammingResult r;
    r.original_len = original_len;
    r.encoded_bits = enc;
    r.decoded_bits = dec.substr(0, original_len);
    r.data_bits = r.decoded_bits;
    r.corrected_blocks = corrected;
    r.ok = true;
    return r;
}
inline const std::array<uint8_t, 512>& rs_exp_table() {
    static const std::array<uint8_t, 512> exp_table = []() {
        std::array<uint8_t, 512> t{};
        uint16_t x = 1;
        for (int i = 0; i < 255; ++i) {
            t[i] = static_cast<uint8_t>(x);
            x <<= 1;
            if (x & 0x100) x ^= 0x11d;
        }
        for (int i = 255; i < 512; ++i) t[i] = t[i - 255];
        return t;
    }();
    return exp_table;
}

inline const std::array<uint8_t, 256>& rs_log_table() {
    static const std::array<uint8_t, 256> log_table = []() {
        std::array<uint8_t, 256> t{};
        auto exp = rs_exp_table();
        for (int i = 0; i < 255; ++i) t[exp[i]] = static_cast<uint8_t>(i);
        t[0] = 0;
        return t;
    }();
    return log_table;
}

inline uint8_t rs_gf_mul(uint8_t a, uint8_t b) {
    if (a == 0 || b == 0) return 0;
    const auto& exp = rs_exp_table();
    const auto& log = rs_log_table();
    return exp[static_cast<int>(log[a]) + static_cast<int>(log[b])];
}

inline std::vector<uint8_t> rs_poly_mul(const std::vector<uint8_t>& a,
                                        const std::vector<uint8_t>& b) {
    std::vector<uint8_t> out(a.size() + b.size() - 1, 0);
    for (size_t i = 0; i < a.size(); ++i) {
        for (size_t j = 0; j < b.size(); ++j)
            out[i + j] ^= rs_gf_mul(a[i], b[j]);
    }
    return out;
}

inline std::vector<uint8_t> rs_generator_poly(int nsym) {
    if (nsym <= 0 || nsym > 32)
        throw std::invalid_argument("Reed-Solomon: parity symbols (nsym) must be in 1..32");
    std::vector<uint8_t> g{1};
    const auto& exp = rs_exp_table();
    for (int i = 0; i < nsym; ++i) {
        std::vector<uint8_t> term{1, exp[i]};
        g = rs_poly_mul(g, term);
    }
    return g;
}

inline std::string rs_compute_parity(const std::string& data_bytes, int nsym) {
    if (data_bytes.empty())
        throw std::invalid_argument("Reed-Solomon: data must not be empty");

    auto gen = rs_generator_poly(nsym);
    std::vector<uint8_t> msg(data_bytes.begin(), data_bytes.end());
    msg.resize(data_bytes.size() + static_cast<size_t>(nsym), 0);

    for (size_t i = 0; i < data_bytes.size(); ++i) {
        uint8_t coef = msg[i];
        if (coef != 0) {
            for (size_t j = 1; j < gen.size(); ++j)
                msg[i + j] ^= rs_gf_mul(gen[j], coef);
        }
    }

    return std::string(msg.end() - nsym, msg.end());
}

inline bool rs_verify_codeword(const std::string& codeword, int nsym) {
    if (codeword.empty()) return false;
    const auto& exp = rs_exp_table();

    for (int i = 0; i < nsym; ++i) {
        uint8_t s = 0;
        uint8_t x = exp[i];
        for (unsigned char b : codeword)
            s = static_cast<uint8_t>(rs_gf_mul(s, x) ^ b);
        if (s != 0) return false;
    }
    return true;
}

struct ReedSolomonResult {
    std::string bits;
    std::string packed_bytes;
    std::string parity_bytes;
    int         nsym;
    bool        ok;
};

inline ReedSolomonResult reed_solomon_encode(const std::string& bits, int nsym) {
    validate_bit_string(bits, "Reed-Solomon");
    if (bits.size() > 65535)
        throw std::invalid_argument("Reed-Solomon: max bit length is 65535 for this packet format");

    ReedSolomonResult r;
    r.bits = bits;
    r.nsym = nsym;
    r.packed_bytes = pack_bits_to_bytes(bits);
    r.parity_bytes = rs_compute_parity(r.packed_bytes, nsym);
    r.ok = true;
    return r;
}

inline std::string reed_solomon_pack(const ReedSolomonResult& r) {
    if (r.nsym <= 0 || r.nsym > 255)
        throw std::invalid_argument("Reed-Solomon: nsym must be in 1..255 for packet format");
    std::string out;
    uint16_t bit_len = static_cast<uint16_t>(r.bits.size());
    out += static_cast<char>((bit_len >> 8) & 0xFF);
    out += static_cast<char>(bit_len & 0xFF);
    out += static_cast<char>(r.nsym & 0xFF);
    out += r.packed_bytes;
    out += r.parity_bytes;
    return out;
}

inline ReedSolomonResult reed_solomon_decode(const std::string& wire) {
    if (wire.size() < 4)
        throw std::runtime_error("Reed-Solomon: packet too short");

    uint16_t bit_len = (static_cast<uint8_t>(wire[0]) << 8)
                     |  static_cast<uint8_t>(wire[1]);
    if (bit_len == 0)
        throw std::runtime_error("Reed-Solomon: invalid bit length in packet");

    int nsym = static_cast<uint8_t>(wire[2]);
    if (nsym <= 0)
        throw std::runtime_error("Reed-Solomon: invalid nsym in packet");

    size_t data_len = (bit_len + 7) / 8;
    if (wire.size() < 3 + data_len + static_cast<size_t>(nsym))
        throw std::runtime_error("Reed-Solomon: truncated packet");

    std::string packed = wire.substr(3, data_len);
    std::string parity = wire.substr(3 + data_len, static_cast<size_t>(nsym));

    ReedSolomonResult r;
    r.bits = unpack_bytes_to_bits(packed, bit_len);
    r.packed_bytes = packed;
    r.parity_bytes = parity;
    r.nsym = nsym;
    r.ok = rs_verify_codeword(packed + parity, nsym);
    return r;
}
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
