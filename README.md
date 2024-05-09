# Plox Interpreter

Plox is a simple interpreter for the lox programming language. It is capable of interpreting lox programs containing various statements and expressions.

## Usage

Lox interpreter provides a convenient way to run Lox programs from the command line or interactively. Here's a brief description of its usage:

#### Run a Lox Script File
+ You can execute a Lox script file by providing its path as a command-line argument to the lox.py script.

    ```bash
    python lox.py <script_file>
    ```

#### Interactive Mode
+ If you want to run Lox interactively, without a script file, you can enter Lox commands directly in the terminal.
    
    ```bash
    python lox.py
    ```
  *This opens an interactive prompt where you can type Lox commands one at a time. To exit interactive mode, press Ctrl + C.*


## Features

### Supported statements

Lox supports the following types of statements:

+ **Variable Declarations (`var`)**
+ **Function Declarations (`fun`)**
+ **Class Declarations (`class`)**
+ **Expression Statements**
+ **Print Statements (`print`)**
+ **Block Statements**
+ **If Statements (`if`, `else`)**
+ **While Statements (`while`)**
+ **For Statements (`for`)**
+ **Return Statements (`return`)**


### Supported Expressions

Lox supports the following types of expressions:

+ **Assignment Expressions (`=`)**
+ **Logical `OR` and `AND` Expressions (`or`, `and`)**
+ **Equality Expressions (`!=` `==`)**
+ **Comparison Expressions (`>`, `>=`, `<`, `<=`)**
+ **Arithmetic Expressions (`+`, `-`, `\*`, `/`)**
+ **Unary Expressions (`!`, `-`)**
+ **Function Call Expressions**
+ **Primary Expressions (`true`, `false`, `nil`, `numbers`, `strings`, `identifiers`)**


### Examples

*Here's an example Lox code that finds Fibonacci numbers up to 20:*

```bash
fun fib(n) {
     if (n <= 1) return n;
         return fib(n - 2) + fib(n - 1);
    }
    for (var i = 0; i < 20; i = i + 1) {
         print fib(i);
    }
```

*Here's counter function, which store count in var and print it:*

```bash
fun makeCounter() {
    var i = 0;
    fun count() {
        i = i + 1;
        print i;
    }
    return count;
}
var counter = makeCounter();
counter(); //1
counter(); //2
counter(); //3
```
