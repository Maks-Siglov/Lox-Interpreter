#ifndef clox_compiler_h
#define clox_compiler_h

#include "vm.h"
#include "scanner.h"

typedef enum {
    PREC_NONE,
    PREC_ASSIGNMENT, // =
    PREC_OR, // or
    PREC_AND, // and
    PREC_EQUALITY, // == !=
    PREC_COMPARISON, // < > <= >=
    PREC_TERM, // + -
    PREC_FACTOR, // * /
    PREC_UNARY, // ! -
    PREC_CALL, // . ()
    PREC_PRIMARY
} Precedence;

typedef void (*ParseFn)();

typedef struct {
    ParseFn prefix;
    ParseFn infix;
    Precedence precedence;
} ParseRule;

bool compile(const char* source, Chunk* chunk);

static void advance();
static void consume(TokenType type, const char* message);
static void emitBytes(uint8_t byte1, uint8_t byte2);
static void emitByte(uint8_t byte);
static Chunk* currentChunk();
static void endCompiler();
static void emitReturn();
static void expression();
static void number();
static void emitConstant(Value value);
static uint8_t makeConstant(Value value);
static void grouping();
static void unary();
static void binary();
static void parsePrecedence(Precedence precedence);
static ParseRule* getRule(TokenType type);
static void errorAtCurrent(const char* message);
static void error(const char* message);
static void errorAt(Token* token, const char* message);

#endif