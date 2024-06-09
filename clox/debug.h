#ifndef clox_debug_h
#define clox_debug_h

#include "scanner.h"
#include "chunk.h"

void disassembleChunk(Chunk* chunk, const char* name);
int disassembleInstruction(Chunk* chunk, int offset);

const char* getTokenTypeName(TokenType type);

#endif