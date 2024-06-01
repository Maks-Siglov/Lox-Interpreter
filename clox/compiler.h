#ifndef clox_compiler_h
#define clox_compiler_h

#include "vm.h"
#include "scanner.h"

bool compile(const char* source, Chunk* chunk);
static void advance();
static void expression();
static void consume(TokenType type, const char* message);
static void emitBytes(uint8_t byte1, uint8_t byte2);
static void emitByte(uint8_t byte);
static Chunk* currentChunk();
static void endCompiler();
static void emitReturn();
static void errorAtCurrent(const char* message);
static void error(const char* message);
static void errorAt(Token* token, const char* message);

#endif
