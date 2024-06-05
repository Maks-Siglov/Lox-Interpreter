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

static Chunk* currentChunk();

bool compile(const char* source, Chunk* chunk);

static void advance();
static void consume(TokenType type, const char* message);

static void emitBytes(uint8_t byte1, uint8_t byte2);
static void emitByte(uint8_t byte);
static void endCompiler();
static void emitReturn();

static void expression();
static void declatration();
static void statement();
static void printStatement();
static void expressionStatement();
static void varDeclaration();
static uint8_t parseVariable(const char* errorMessage);
static uint8_t identifierConstant(Token* name);
static void defineVariable(uint8_t global);


static void number();
static void string();
static void variable();
static void namedVariable(Token name);

static bool match(TokenType type);
static bool check(TokenType type);

static void emitConstant(Value value);
static uint8_t makeConstant(Value value);

static void grouping();
static void unary();
static void binary();
static void literal();

static void parsePrecedence(Precedence precedence);
static ParseRule* getRule(TokenType type);

static void synchronize();
static void errorAtCurrent(const char* message);
static void error(const char* message);
static void errorAt(Token* token, const char* message);

#endif