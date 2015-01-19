// Copyright 2013-2015 the openage authors. See copying.md for legal info.

#ifndef OPENAGE_UTIL_FILE_H_
#define OPENAGE_UTIL_FILE_H_

#include <cinttypes>
#include <cstring>
#include <string>
#include <vector>

#include "error.h"
#include "dir.h"
#include "../log.h"

namespace openage {
namespace util {

/** Returns whether the given file exists. */
bool file_exists(const char *filename);

/** Returns whether the given file exists. */
bool file_exists(const std::string &filename);

/** Returns the whole content of the given file. */
std::vector<char> read_whole_file(const char *filename);

/** Returns the whole content of the given file. */
std::vector<char> read_whole_file(const std::string &filename);

/** Returns all lines from the given file. */
std::vector<std::string> read_lines_from_file(const char *filename);

/** Returns all lines from the given file. */
std::vector<std::string> read_lines_from_file(const std::string &filename);

/**
 * read a single csv file.
 * call the destination struct .fill() method for actually storing line data
 */
template <class lineformat>
std::vector<lineformat> read_csv_file(const std::string &fname) {
	std::vector<std::string> lines = read_lines_from_file(fname);

	size_t line_count = 0;

	lineformat current_line_data;
	auto result = std::vector<lineformat>{};

	for (auto &line : lines) {
		int line_length = line.length();
		line_count += 1;

		//ignore empty and lines starting with #, that's a comment.
		if (line_length > 0 && line[0] != '#') {

			//create writable tokenisation copy of the string
			char *line_rw = new char[line_length + 1];
			strncpy(line_rw, line.c_str(), line_length);
			line_rw[line_length] = '\0';

			//use the line copy to fill the current line struct.
			int error_column = current_line_data.fill(line_rw);
			if (error_column != -1) {
				throw Error("failed reading csv file %s in line %" PRIuPTR " column %d: error parsing '%s'",
				            fname.c_str(), static_cast<uintptr_t>(line_count), error_column,
				            line.c_str());
			}

			delete[] line_rw;

			result.push_back(current_line_data);
		}
	}

	return result;
}

/**
 * reads data files recursively.
 * should be called from the .recurse() method of the struct.
 */
template <class lineformat>
std::vector<lineformat> recurse_data_files(Dir basedir, const std::string &fname) {
	std::vector<lineformat> result;
	std::string merged_filename = basedir.join(fname);

	if (file_exists(merged_filename)) {
		result = read_csv_file<lineformat>(merged_filename);

		//the new basedir is the old basedir
		// + the directory part of the current relative file name
		Dir new_basedir = basedir.append(dirname(fname));

		size_t line_count = 0;
		for (auto &entry : result) {
			line_count += 1;
			if (not entry.recurse(new_basedir)) {
				throw Error("failed reading follow up files for %s in line %" PRIuPTR,
				            merged_filename.c_str(), static_cast<uintptr_t>(line_count));
			}
		}
	}
	else {
		//nonexistant file skipped, would return empty vector.
		throw Error("failed recursing to file %s", merged_filename.c_str());
	}

	return result;
}


template <class lineformat>
std::vector<lineformat> read_csv_file(const char *fname) {
	std::string filename{fname};
	return read_csv_file<lineformat>(filename);
}

/**
 * referenced file tree structure.
 *
 * used to store the filename and resulting data of a file down
 * the gamedata tree.
 */
template <class cls>
struct subdata {
	std::string filename;
	std::vector<cls> data;

	bool read(Dir basedir) {
		this->data = recurse_data_files<cls>(basedir, this->filename);
		return true;
	}

	cls operator [](size_t idx) const {
		return this->data[idx];
	}
};


} //namespace util
} //namespace openage

#endif
