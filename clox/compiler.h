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


typedef void (*ParseFn)(bool canAssign);

typedef struct {
    ParseFn prefix;
    ParseFn infix;
    Precedence precedence;
} ParseRule;

typedef struct {
    Token name;
    int depth;
} Local;

typedef struct {
    Local locals[UINT8_COUNT];
    int localCount;
    int scopeDepth;
} Compiler;

static Chunk* currentChunk();

bool compile(const char* source, Chunk* chunk);

static void initCompiler(Compiler* compiler);

static void advance();
static void consume(TokenType type, const char* message);

static void emitBytes(uint8_t byte1, uint8_t byte2);
static void emitByte(uint8_t byte);
static void endCompiler();
static void emitReturn();

static void expression();
static void declaration();
static void statement();

static void printStatement();
static void expressionStatement();
static void ifStatement();

static void and_(bool canAssign);
static void or_(bool canAssign);

static void grouping(bool canAssign);
static void unary(bool canAssign);
static void binary(bool canAssign);
static void literal(bool canAssign);

static void block();
static void beginScope();
static void endScope();

static void varDeclaration();
static void declareVariable();
static void addLocal(Token name);
static bool identifiersEqual(Token* a, Token* b);
static int resolveLocal(Compiler* compiler, Token* name);
static void markInitialized();

static uint8_t parseVariable(const char* errorMessage);
static uint8_t identifierConstant(Token* name);
static void defineVariable(uint8_t global);


static void number(bool canAssign);
static void string(bool canAssign);
static void variable(bool canAssign);
static void namedVariable(Token name, bool canAssign);

static bool match(TokenType type);
static bool check(TokenType type);

static void emitConstant(Value value);
static uint8_t makeConstant(Value value);
static int emitJump(uint8_t instruction);

static void patchJump(int offset);

static void parsePrecedence(Precedence precedence);
static ParseRule* getRule(TokenType type);

static void synchronize();
static void errorAtCurrent(const char* message);
static void error(const char* message);
static void errorAt(Token* token, const char* message);

#endif