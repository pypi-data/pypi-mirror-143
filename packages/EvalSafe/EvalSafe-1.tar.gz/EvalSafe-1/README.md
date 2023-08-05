# EvalSafe
EvalSafe is my small library for python. It's library help you with Calculate expressions in a string using eval without security threats.

(I do not know who needs it, I did it out of boredom)

# Example of using

## If digital data is entered
```import evalsafe```

```print(evalsafe.evals("5 + 5 + 5"))```

**Result: 15**

## If a command from python is entered

```import evalsafe```

```print(evalsafe.evals("print('text')"))```

**Result: Error, incorrect value entered!**