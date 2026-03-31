#pragma once
#include <string>
#include <vector>
#include <stdexcept>
#include <sstream>

// ─────────────────────────────────────────────
//  Constants
// ─────────────────────────────────────────────
static const std::string BYTE_FLAG = "FLAG";
static const std::string BYTE_ESC  = "ESC";
static const std::string BIT_FLAG  = "01111110";

// ─────────────────────────────────────────────
//  1. Character Count Framing
// ─────────────────────────────────────────────

// Encode: splits data into frames of (total_frame_size - 1) payload bytes.
// Each frame is: [count][payload...]  where count = payload_len + 1
std::vector<std::string> character_count_encode(const std::string& data,
                                                int total_frame_size = 5) {
    if (total_frame_size <= 1)
        throw std::invalid_argument("total_frame_size must be > 1");

    int payload_size = total_frame_size - 1;
    std::vector<std::string> frames;

    for (int i = 0; i < (int)data.size(); i += payload_size) {
        std::string payload = data.substr(i, payload_size);
        char count = (char)(payload.size() + 1); // count includes itself
        frames.push_back(std::string(1, count) + payload);
    }
    return frames;
}

// Decode: read count byte, then count-1 payload bytes, repeat.
std::string character_count_decode(const std::string& raw) {
    std::string result;
    int i = 0;
    while (i < (int)raw.size()) {
        int count = (unsigned char)raw[i];
        if (count < 1)
            throw std::runtime_error("Character count decode: invalid count byte");
        int payload_len = count - 1;
        if (i + count > (int)raw.size())
            throw std::runtime_error("Character count decode: truncated frame");
        result += raw.substr(i + 1, payload_len);
        i += count;
    }
    return result;
}

// ─────────────────────────────────────────────
//  2. Byte Stuffing
//  Protocol:  FLAG <stuffed-data> FLAG
//  Stuffing:  ESC → ESC ESC
//             FLAG (inside data) → ESC FLAG
// ─────────────────────────────────────────────

std::string byte_stuff(const std::string& data) {
    // Order matters: escape ESC first, then FLAG
    std::string stuffed;
    stuffed.reserve(data.size() * 2);

    // We need to scan character by character to avoid double-replacing
    size_t i = 0;
    while (i < data.size()) {
        // Check for ESC first
        if (data.compare(i, BYTE_ESC.size(), BYTE_ESC) == 0) {
            stuffed += BYTE_ESC + BYTE_ESC;
            i += BYTE_ESC.size();
        }
        // Then FLAG
        else if (data.compare(i, BYTE_FLAG.size(), BYTE_FLAG) == 0) {
            stuffed += BYTE_ESC + BYTE_FLAG;
            i += BYTE_FLAG.size();
        }
        else {
            stuffed += data[i];
            i++;
        }
    }
    return BYTE_FLAG + stuffed + BYTE_FLAG;
}

std::string byte_unstuff(const std::string& framed) {
    // Verify and strip outer FLAGs
    if (framed.compare(0, BYTE_FLAG.size(), BYTE_FLAG) != 0 ||
        framed.compare(framed.size() - BYTE_FLAG.size(), BYTE_FLAG.size(), BYTE_FLAG) != 0) {
        throw std::runtime_error("Byte unstuff: missing FLAG delimiters");
    }

    // Inner content between the two FLAGs
    std::string inner = framed.substr(BYTE_FLAG.size(),
                                      framed.size() - 2 * BYTE_FLAG.size());
    std::string result;
    size_t i = 0;
    while (i < inner.size()) {
        if (inner.compare(i, BYTE_ESC.size(), BYTE_ESC) == 0) {
            i += BYTE_ESC.size();
            if (i >= inner.size())
                throw std::runtime_error("Byte unstuff: ESC at end of data");
            // Next token is either ESC or FLAG
            if (inner.compare(i, BYTE_ESC.size(), BYTE_ESC) == 0) {
                result += BYTE_ESC;
                i += BYTE_ESC.size();
            } else if (inner.compare(i, BYTE_FLAG.size(), BYTE_FLAG) == 0) {
                result += BYTE_FLAG;
                i += BYTE_FLAG.size();
            } else {
                throw std::runtime_error("Byte unstuff: unexpected ESC sequence");
            }
        } else {
            result += inner[i];
            i++;
        }
    }
    return result;
}

// ─────────────────────────────────────────────
//  3. Bit Stuffing
//  Protocol:  01111110 <stuffed-bits> 01111110
//  Stuffing:  After 5 consecutive 1s, insert a 0
// ─────────────────────────────────────────────

std::string bit_stuff(const std::string& bits) {
    for (char c : bits)
        if (c != '0' && c != '1')
            throw std::invalid_argument("Bit stuffing: input must be only 0s and 1s");

    std::string stuffed;
    int ones = 0;
    for (char b : bits) {
        stuffed += b;
        if (b == '1') {
            ones++;
            if (ones == 5) { stuffed += '0'; ones = 0; }
        } else {
            ones = 0;
        }
    }
    return BIT_FLAG + stuffed + BIT_FLAG;
}

std::string bit_unstuff(const std::string& framed) {
    if (framed.compare(0, BIT_FLAG.size(), BIT_FLAG) != 0 ||
        framed.compare(framed.size() - BIT_FLAG.size(), BIT_FLAG.size(), BIT_FLAG) != 0) {
        throw std::runtime_error("Bit unstuff: missing flag delimiters");
    }

    std::string inner = framed.substr(BIT_FLAG.size(),
                                      framed.size() - 2 * BIT_FLAG.size());
    std::string result;
    int ones = 0;
    size_t i = 0;
    while (i < inner.size()) {
        char b = inner[i];
        if (b == '1') {
            result += b;
            ones++;
            if (ones == 5) {
                i++; // skip the stuffed 0
                if (i < inner.size() && inner[i] != '0')
                    throw std::runtime_error("Bit unstuff: expected stuffed 0");
                ones = 0;
            }
        } else {
            result += b;
            ones = 0;
        }
        i++;
    }
    return result;
}