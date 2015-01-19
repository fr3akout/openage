// Copyright 2013-2015 the openage authors. See copying.md for legal info.

#include "file.h"

#include <fstream>

#include "../log.h"
#include "error.h"

namespace openage {
namespace util {

bool file_exists(const char *filename) {
	std::ifstream fin{filename};
	return fin.good();
}

bool file_exists(const std::string &filename) {
	return file_exists(filename.c_str());
}

std::vector<char> read_whole_file(const char *filename) {
	std::ifstream fin{filename, std::ios::binary};
	if (not fin.good()) {
		throw Error{"Failed to open file: %s", filename};
	}

	std::vector<char> result{std::istreambuf_iterator<char>{fin},
			std::istreambuf_iterator<char>{}};
	return std::move(result);
}

std::vector<char> read_whole_file(const std::string &filename) {
	return std::move(read_whole_file(filename.c_str()));
}

std::vector<std::string> read_lines_from_file(const char *filename) {
	std::ifstream fin{filename};
	if (not fin.good()) {
		throw Error{"Failed to open file: %s", filename};
	}

	std::vector<std::string> lines;
	std::string line;
	while (std::getline(fin, line)) {
		lines.push_back(line);
	}
	return std::move(lines);
}

std::vector<std::string> read_lines_from_file(const std::string &filename) {
	return std::move(read_lines_from_file(filename.c_str()));
}

} //namespace util
} //namespace openage
