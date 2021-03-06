// Copyright 2013-2015 the openage authors. See copying.md for legal info.

#include "shader.h"

#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>

#include "../error/error.h"
#include "../log/log.h"
#include "../util/file.h"
#include "../util/strings.h"

namespace openage {
namespace shader {

const char *type_to_string(GLenum type) {
	switch (type) {
	case GL_VERTEX_SHADER:
		return "vertex";
	case GL_FRAGMENT_SHADER:
		return "fragment";
	case GL_GEOMETRY_SHADER:
		return "geometry";
	default:
		return "unknown";
	}
}

Shader::Shader(GLenum type, const char *source) {
	//create shader
	this->id = glCreateShader(type);

	//store type
	this->type = type;

	//load shader source
	glShaderSource(this->id, 1, &source, NULL);

	//compile shader source
	glCompileShader(this->id);

	//check compiliation result
	GLint status;
	glGetShaderiv(this->id, GL_COMPILE_STATUS, &status);

	if (status != GL_TRUE) {
		GLint loglen;
		glGetShaderiv(this->id, GL_INFO_LOG_LENGTH, &loglen);

		auto infolog = std::make_unique<char[]>(loglen);
		glGetShaderInfoLog(this->id, loglen, NULL, infolog.get());

		auto errmsg = MSG(err);
		errmsg << "Failed to compile " << type_to_string(type) << " shader\n" << infolog;

		glDeleteShader(this->id);

		throw Error(errmsg);
	}
}

Shader::~Shader() {
	glDeleteShader(this->id);
}

} //namespace shader
} //namespace openage
