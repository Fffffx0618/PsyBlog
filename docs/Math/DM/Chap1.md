# Ch1.Logic & Proofs

## 1.1 Propositional Logic

### 1. Propositions

<u>A proposition is a **declarative sentence** (that is, a sentence that declares a fact) that is either `true` or `false`, but not both.</u>

- **Paradox (悖论)** 不属于命题（e.g. *This statement is false.* or *I'm lying.*）

**Propositional variable / Sentential variables (命题变量)**：Small letters such as $p,q,r,s,\dots$ used to present propositions.

**Propositional logic / Propositional calculus (命题逻辑)**：The area of logic that deals with propositions.

**Truth value(真值)**：T (true proposition), or F (false proposition)

We call a series of propositions **==consistent== (一致的)** if they can possibly be satisfied at the same time.

### 2. Connectives

#### Logical Operators

**Logical operator** or **Logical Connective**: be used to form **compound propositions** from existing propositions.

| Connectives                           | Expression |               Note               |
| :------------------------------------ | :--------: | :------------------------------: |
| negation (NOT)                        |    $¬p$    | $~p, -p, p', Np, \text{and } !p$ |
| 和取 conjunction (AND)                |   $p\land q$    |          "but" = "and"           |
| 析取 disjunction (OR)                 |   $p\lor q$    |         an inclusive or          |
| 亦或 Exclusive Or (XOR)               |   $p⊕q$    |         an exclusive or          |
| 条件 Conditional (IF-THEN)            |   $p\rightarrow q$    |                                  |
| 双条件 Biconditional (IF AND ONLY IF) |   $p↔q$    |           参见下节介绍           |

- 英语中的单词 or 既可以表示 **inclusive or** 也可以表示 **exclusive or**（e.g. *George was born in 1956 or 1957.*），取决于具体语境。

逻辑运算符的**优先级(precedence)** 如下：

|  ¬   | \land  |\lor  | \rightarrow  | ↔ |
| :--: | :--: | :--: | :--: | :--: |
|  1   |   2   |   3   |   4   |   5   |

####  Conditional Statements

==**Implication** or **Conditional statement**== ：$p\rightarrow q$ is false when $p$ is true and $q$ is false, and true otherwise.

- **p :** **假设(hypothesis / antecedent / premise)**
- **q :** **结论(conclusion / consequence)**


对于推断 p\rightarrow q可定义以下条件语句：

- **Converse (逆命题)**：$q\rightarrow p$
- **Inverse (否命题)**：$¬p\rightarrow ¬q$
- **Contrapositive (逆否命题)**：$¬q\rightarrow ¬p$


When two compound propositions always have the same truth values, regardless of the truth values of its propositional variables, we call them **==equivalent==（等价的）**.

* The ***contrapositive*** has the **same** truth values as the original implication.

* The ***converse*** and the ***inverse*** of a conditional statement are also **equivalent**.

**==Biconditional statement (双条件语句)==**：The biconditional statement p↔q is the propostion “p if and only if q.” 

### 3. Truth Table

要学会画**真值表(truth table)**。

- n个不同的布尔变量所画的真值表应有 $2^{n}$ 行。

### 4. Logic and Bit Operatons

**Bit**: a symbol with two possible values , namely, 0 and 1.

**Boolean variable**: one whose value is either true or false.

## 1.2 Applications of Propositional Logic

* Translating English to Propositional Logic

* System Specifications

    * System specifications should be **consistent**.

* Logic Puzzles

## 1.3 Propositional Equivalences

### 1. Introduction

* A **tautology (永真)** is a proposition which is always true.  Example: $p \lor ¬p$
* A **contradiction (永假)** is a proposition which is always false.  Example: $p \land ¬p$
* A **contingency (可能式)** is a proposition which is neither a tautology nor a  contradiction, such as $p$

**Propositional Satisfiability**

* A compound proposition is **==satisfiable==** if there is an assignment of truth values to its  variables that makes it true. 
* A compound proposition is **==unsatisfiable==** when it is false for all assignments of truth  values to its variables.

**Equivalent**

* The propositions $p$ and $q$ are called ==**logically equivalent（逻辑等值）**== if $p ↔ q$ is a  tautology.

* Notation: $p ⇔ q$ or $p \equiv  q$

**Other logical operators**

* <u>Sheffer stroke</u> |:  $p|q \equiv  ¬(p \land  q)$ NAND 
* <u>Peirce arrow</u> ↓:  $p ↓ q \equiv  ¬(p \lor  q)$ NOR

### 2. Logical Laws

- 可以用真值表来证明一些基本的逻辑定律：对于涉及到$n$个变量的两个命题，画出 $2^n$ 种可能的变量取值下的真值表，若两个命题的值都相同，则说明这两个命题是逻辑等值的。

  | Name                           |                     Expression                     | Note                   |
  | :----------------------------- | :------------------------------------------------: | :--------------------- |
  | 统一律 Identity Laws           |               $p\land T \equiv  p$   $p\lor F \equiv  p$                |                        |
  | 零一律 Domination Laws         |               $p\lor T \equiv  T$   $p\land F \equiv  F$                |                        |
  | 幂等律 Idempotent Laws         |               $p\land p \equiv  p$   $p\lor p \equiv  p$                |                        |
  | 对合律 Double Negation Law     |                     $¬¬p \equiv  p$                      |                        |
  | 交换律 Commutative Laws        |             $p\lor q \equiv  q\lor p$   $p\land q \equiv  q\land p$              |                        |
  | 结合律 Associative Laws        |     $(p\lor q)\lor r \equiv  p\lor (q\lor r)$    $(p\land q)\land r \equiv  p\land (q\land r)$     |                        |
  | 分配律 Distributive Laws       | $p\lor (q\land r) \equiv  (p\lor q)\land (p\lor r)$   $ p\land (q\lor r) \equiv  (p\land q)\lor (p\land r)$ |                        |
  | **德·摩根律 De Morgan's Laws** |        $¬(p\lor q) \equiv  ¬p\land ¬q$    $¬(p\land q) = ¬p\lor ¬q$        | **重要**               |
  | 否定律 Negation Laws           |              $p\lor ¬p \equiv  T$   $p\land ¬p \equiv  F$               |                        |
  | 吸收律 Absorption Laws         |           $p\lor (p\land q) \equiv  p$   $p\land (p\lor q) \equiv  p$            |                        |
  | 逆否律 Contrapositive Laws     |                   $p\rightarrow q \equiv  ¬q\rightarrow ¬p$                    | 命题与它的逆否命题等价 |
  | **导出律 Exportation Laws**    |                $(p\land q)\rightarrow r \equiv  p\rightarrow (q\rightarrow r)$                 |                        |
  | Absurdity Laws                 |                $(p\rightarrow q)\land (p\rightarrow ¬q) \equiv  ¬p$                 |                        |
  | **蕴含律 Implication Laws**    |                    $p\rightarrow q \equiv  ¬p\lor q$                    | 用于去掉箭头           |
  | Equivalence Laws               |                $p↔q \equiv  (p\rightarrow q)\land (q\rightarrow p)$                 |                        |
### 3. The Dual of a Compound Proposition 

The **dual对偶** of compound proposition that contains only the logical operators  $\lor $ , $\land $ and $¬$ is the proposition obtained by replacing each $\lor $ by $\land $,each $\land $ by $\lor $,each $T$ by $F$ and each $F$ by $T$. The dual of $S$ is denoted by $S^{*}$.  

*  $S = (p \lor  ¬q) \land  r \lor  T$      $S^{*} = (p \land  ¬q) \lor  r \land  F$

* $S = (p \land  q) \rightarrow  (p \lor  q) \equiv  ¬(p \land  q) \lor  (p \lor  q)$     $S^{*} = ¬(p \lor  q) \land  (p \land  q)$ 

【Theorem】 let $s$ and $t$ are two compound propositions, **$s$ \equiv  $t$ if and  only if $s^*$ \equiv  $t^*$** .

### 4. Functionally Complete Collection of Logical Operators 

只需要部分运算符就可以表示出所有可能的运算，

称这样的一个运算符集合为**全功能集(Functionally Complete Collection)**

**极小全功能集**：$\{¬,\lor ,\land ,\rightarrow ,↔ \}\{¬,\lor ,\land \}, \{¬,\land \}\{¬,\lor \}, \{∣\}, \{↓\}$ 等。

> * $p\lor q\equiv ¬(¬p\land ¬q)$
> * $¬p\equiv p∣p$
> * $p\land q\equiv ¬(p∣q)\equiv (p∣q)∣(p∣q)$
> * $p\lor q\equiv ¬(¬p\land ¬q)\equiv ¬p∣¬q\equiv (p∣p)∣(q∣q)$

### 5. Propositional Normal Forms

####  5.1 DNF/CNF

- A **字面量(literal)** is a variable or its negation.
- Conjunctions with literals as conjuncts are called **合取子句(conjunctive clauses)** (clauses). <u>通过 AND 连接起来的一组字面量</u>。

**Propositional Normal Forms**：

- **析取范式(Disjunctive Normal Form, DNF)**

    A formula is said to be in **disjunctive normal form** if it is written as a disjunction, in which all the terms are conjunctions of literals. 

    > e.g.  $(p\land q)\lor (p\land ¬q)$
    >
    > - 最外面一层的运算符都是析取 $\lor$
    > - 括号内的运算符都是合取 $\land$

- **合取范式(Conjunctive Normal Form, CNF)**

    > e.g. $(p \lor  q)\land (p\lor ¬q)$
  
  和 DNF 的定义相反；把 $\land $ 和 $\lor $ 互换。

#### 5.2 Full DNF & Full CNF

- **Minterm(极小项)** : a conjunctive of literals in which each variable is represented <u>exactly once</u>.
- **Maxterm(极大项)** : a disjunctive of literals in which each variable is represented <u>exactly once</u>.

**Full Disjunctive Normal Form(主析取范式)**：

> e.g. $(p\land \neg q \land r)\lor(\neg p \land q \land r)\lor (p \land q \land r)=\sum m(3,5,7)$

If a formula is expressed as a disjunction of minterms, it is said to be in **full disjunctive normal form**.

- 每个最小项对应真值表中 $T$ 的恰好一行。

**Full Conjuctive Normal Form(主合取范式)**：

> e.g. $(p\lor \neg q \lor r)\land(\neg p \lor q \lor r)\land (p \lor q \lor r)=\sum M(0,2,4)$

- 取出所有真值表为中为 F 的位置，写出 $¬f$。
- 对 $¬f$ 应用 De Morgan's Laws，可以将式子中的合取析取互换，从而求得 FCNF。

## 1.4 Predicates and Quantifiers

###  1. Predicates

- **Propositional functions命题函数** become propositions (and have truth values) when <u>their variables are each replaced by a value from the domain</u> or <u>bound by a quantifier</u>. 

- The statement $P(x_{1}, x_{2}, x_{3})$ is said to be the value of the propositional function $P$ at $x_{1}, x_{2}, x_{3}$. 

-  A statement of the form  $P(x_{1}, x_{2}, x_{3})$ is the value of the propositional function $P$ at the $n-tuple \space (x_1,x_2,…, x_n)$ and $P$ is called **a n-ary predicate n位谓词**.

Predicates are also used to establish the correctness of computer programs. 

  * **preconditions前置条件** : the statements that describe **valid input** 
  * **postconditions后置条件** : the conditions that the **output** should satisfy when the  program has run

### 2. Quantifiers

**全称量词(universal quantifier)** $\forall$ ：都是真才为真，存在一个为假就为假。可以转化为合取。

**存在量词(existential quantifier)** $\exists$ ：都是假才为假，存在一个为真就为真。可以转化为析取。

**唯一量词(uniqueless quantifier)** $\exists !$ ：有且仅有一个为真时才为真。

我们在使用量词时，可能只要求对于某一范围内的 $x$ 成立，我们把此时 $x$ 的取值范围称为 **讨论域** (domain of discourse / universe of discourse)，一般简写为 **domain**。

**量词的优先级(precedence of quantifiers)**

* The quantifiers \forall  and \exists  have higher precedence(优先级) than **all** the logical operators.

If t**he domain is finite**, <u>**a universally quantified proposition**</u> is  equivalent to a **conjunction** of propositions without quantifiers and <u>**an existentially quantified proposition**</u> is equivalent to a **disjunction** of  propositions without quantifiers.

### 3. Equivalences in Predicate Logic

Statements involving predicates and quantifiers are logically **equivalent** if and only if they **have the same truth value** no matter

- 代入了什么谓词选择 which predicates are substituted into these statements and
- 使用了什么讨论域 which domain of discourse is used for the variables in these propositional functions

同样使用 $\equiv $ 符号来表示谓词逻辑中的等值。

**德摩根定律(De Morgan's laws)** 在谓词逻辑中也适用：

* $¬\forall xP(x)\equiv \exists x¬P(x)$

* $¬\exists xP(x)\equiv \forall x¬P(x)$

只有在 $A(x)$ 和 $B(x)$ 都输出真时，$A(x)\land B(x)$ 才为真，此时第一个等式的两侧都为真，否则两侧都为假。类似的可以证明第二个等式。

* $\forall x(A(x)\land B(x))\equiv \forall xA(x)\land \forall xB(x)$ , $\exists x(A(x)\lor B(x))\equiv \exists xA(x)\lor \exists xB(x)$

但是如果把上面的等式的 $\land $ 和 $\lor $ 互换则不成立。容易举出反例。

* $\forall x(A(x)\lor B(x))\equiv \forall xA(x)\lor \forall xB(x)$ , $\exists x(A(x)\land B(x))\equiv \exists xA(x)\land \exists xB(x)$

For example, $U$：the set of real numbers，$Q(x)$：$x$ is a rational number，$F(x)$：$x$ is an irrational number

但这两个命题在其中一个方向上是正确的。

* $\forall xA(x)\lor \forall xB(x)⇒\forall x(A(x)\lor B(x))$ , $\exists x(A(x)\land B(x))⇒\exists xA(x)\land \exists xB(x)$

此外，还有：

$x$ is not occurring in $P$.

- $\forall xA(x)\lor P\equiv \forall x(A(x)\lor P) , \forall xA(x)\land P\equiv \forall x(A(x)\land P)$

- $\exists xA(x)\lor P\equiv \exists x(A(x)\lor P) , \exists xA(x)\land P\equiv \exists x(A(x)\land P)$

x is not occurring in $B$.

- $\forall x(B\rightarrow A(x))\equiv B\rightarrow \forall xA(x)$ , $\exists x(B\rightarrow A(x))\equiv B\rightarrow \exists xA(x)$

- $\forall x(A(x)\rightarrow B)\equiv \exists xA(x)\rightarrow B$ , $\exists x(A(x)\rightarrow B)\equiv \forall xA(x)\rightarrow B$

## 1.5 Nested Quantifiers

**嵌套量词**：Nest quantifiers are quantfiers that occur within <u>the scope of other quantifiers</u>.

### 1. Order of Quantifiers

除非所有量词都是 $\forall $ 或所有量词都是 $\exists $，否则量词的顺序是有意义的。

The order of nested quantifiers is **important** unless all the quantifiers are universal quantifiers or all the quantifiers are existential quantifiers.

### 2. Prenex Normal Form

* $Q_{1}x_{1}Q_{2}x_{2}...Q_{n}x_{n}B$, where $Q_{i}(i = 1,2,...n)$ is $\forall $ or $\exists $, $B$ is quantifier free(不含量词的公式).

得到 **PNF**（**前束范式**）的步骤：

1. 消除所有的 $\rightarrow$和$↔$。
2. 向内移动否定符号，注意应用德摩根定律。
3. 对变量进行重命名，确定不同部分的变量不会冲突。
4. 最后，将所有量词移动到最前面。

## 1.6 Rules of Inference

### 1. Arguments

* An **argument（论据）** in propositional logic is a sequence of propositions.  All but the final proposition are called **premises（前提）**. The last statement is the **conclusion（结论）**.

- An **论据(argument)** is a sequence of statements that end with a conclusion

### 2. Valid Arguments & Argument Form

* An **argument（论据）** is **valid**(有效) if the truth of all its **premises（前提）** implies that the <u>conclusion</u> is true.   
* An **argument form** is **valid** if no matter which particular propositions are substituted for the propositional variables in its premises, the conclusion is true if the premises are all true.
    * If the premises are $p_{1}, p_{2}, ...p_{n}$ and the conclusion is $q$ , then $p_{1}\land p_{2}\land ...\land p_{n}\rightarrow q$ is a **tautology**.

### 3. Rules of Inference

#### 1)Modus Ponens 假言推理

Corresponding Tautology :  $(p\land (p\rightarrow q))\rightarrow q$

#### 2)Modus Tollens 取拒式

Corresponding Tautology :  $(¬ q \land (p \rightarrow q))\rightarrow ¬p$

#### 3)Hypothetical Syllogism 假言三段论

 Corresponding Tautology :  $((p \rightarrow q) \land  (q\rightarrow r))\rightarrow (p\rightarrow  r)$

#### 4)Disjunctive Syllogism 析取三段论

 Corresponding Tautology :  $(¬p\land (p \lor q))\rightarrow q$

#### 5)Addition 附加律

Corresponding Tautology :  $p \rightarrow (p \lor q)$

#### 6)Simplification 化简律

Corresponding Tautology :  $(p\land q) \rightarrow  p$

#### 7)Conjunction 合取律

Corresponding Tautology : $(（p） \land  （q）) \rightarrow (p \land  q)$

#### 8)Resolution 消解律

Corresponding Tautology :  $( (p \lor  q)\land (\neg p \lor  r ) ) \rightarrow(q \lor  r)$

- We use **推理准则(rules of inference)** to construct valid arguments

### 4. Build Valid Arguments 

To prove an argument is valid or the conclusion follows logically from the hypotheses（假设）: 

1. Assume the hypotheses are true. 假定所有假设是对的
2. Use **the rules of inference** and **logical equivalences** to  determine that the conclusion is true.

### 5. Fallacies

#### 1）The Fallacy of affirming the conclusion 肯定结论的谬误

Method: Reasoning based on $((p\rightarrow q) \land  q) \rightarrow  p$

#### 2) The Fallacy of denying the hypothesis 否定假设的谬误

Method: Reasoning based on $((p\rightarrow q) \land ¬ p) \rightarrow  ¬ q$

### 6. Handling Quantified Statements 

**Valid arguments for quantified statements** are a sequence of statements. Each statement is either a premise or follows from previous statements by rules of inference.

#### Universal Instantiation (UI) 全称实例

$$
\frac{\forall x P(x)}{\therefore P(c)}
$$

#### Universal Generalization (UG) 全称引入

$$
\frac{P(c) \text{ for an arbitrary } c}{\therefore \forall x P(x)}
$$

#### Existential Instantiation (EI) 存在实例

$$
\frac{\exists x P(x)}{\therefore P(c)\text{ for some element}}
$$

#### Existential Generalization (EG) 存在引入

$$
\frac{P(c)\text{ for some element}}{\therefore \exists xP(x)}
$$

### 7. The mixed use of propositional and quantitative propositional reasoning rules

#### Universal Modus Ponens 全称假言推理

$$
\forall x (P(x) \rightarrow Q(x))\\
\frac{P(a), \text{ where } a \text{ is a particular element in the domain}}{\therefore Q(a)}
$$

#### Universal Modus Tollens 全称取拒式

$$
  \forall x (P(x) \rightarrow Q(x)) \\
\frac{
  \neg Q(a), \text{ where } a \text{ is a particular element in the domain}
}{
  \therefore \neg P(a)
}
$$

## 1.7 Introduction to Proofs

### 1. Some Terminology

**Theorem**（定理）: A statement that can be shown to be true

* **Proposition**（命题）: Less important theorem (also called result / fact)
  
**Proof**（证明）: A valid argument that establishes the truth of a theorem

* **Axioms**（公理）: The underlying assumptions about mathematical structures,  or hypotheses of the theorem to be proved, or previously proved theorems. 
* **Lemma**（引理） : A 'helping theorem' or a result which is needed to prove a theorem. 
* **Corollary**（推论） :A result which follows directly from a theorem.
* **Conjecture**（猜想）:  A statement whose truth value is unknown.

### 2. Formal Proofs

**形式化证明(formal proof)** v.s. **非形式化证明(informal proof)**：

Formal Proofs：

- All steps were supplied
- The rules for each step in the  argument were given

Informal Proofs:

- More than one rule of inference may be used in each step
- Steps may be skipped
- The axioms being assumed and the  rules of inference used are not explicity stated

### 3. Proof Methods

#### 3.1 Direct Proof

**直接证明法(direct proof)** 证明 $p\rightarrow q$：

- 通过**推理规则(rules of inference)**、公理、**逻辑恒等式(logical equivalences)** 等推出$q$也为真。

其余的证明方法都是**间接证明法(indirect proof)**。

#### 3.2 Proof by Contraposition

反证法可以看做对原命题的逆否命题的直接证明，根据逻辑恒等式：$p\rightarrow q\equiv ¬q\rightarrow ¬p$

- 假设 $¬q$ 为真，推出 $¬p$ 也为真（or 推出 $p$ 为假），从而证明原命题。

#### 3.4 Vacuous and Trivial Proof

**空证明(vacuous proof)**：可通过证明 $p$ 为假来证明 $p\rightarrow q$ 为真。

**平凡证明(trivial proof)**：可以通过证明 $q$ 为真来证明 $p\rightarrow q$ 为真。

#### 3.5 Proof by Contradiciton

**归谬证明法**的步骤

- assumes $p$ is false.
-  derives a contradiction, usually of the form $q \land ¬ q$ which  establishes $¬ p \rightarrow F$.

#### 3.6 Proof of Equivalence 

**等价证明法**

(1)To prove the proposition “$p$ if and only if $q$” 

(2)To prove that several propositions $p_{1}, p_{2} ,...,p_{n}$ are equivalent  

* establish the implications $p_{1}\rightarrow  p_{2}, p_{2}\rightarrow p_{3},...,p_{n}\rightarrow p_{1}$  
* $p_{1}↔p_{2}↔...↔p_{n}\equiv (p_{1}\rightarrow p_{2})\land (p_{2}\rightarrow p_{3} )\land ... \land (p_{n}\rightarrow p_{1})$

## 1.8 Proof Method and Strategy

### 1. Proof Method

#### 穷举和分情况证明法 Exhaustive Proof and Proof by Cases

Using the method of proof by cases to show that $(p_{1} \lor  p_{2} \lor …\lor  p_{n}  ) \rightarrow  q$ (穷举证明法)

$(p_{1} \lor  p_{2} \lor ...\lor p_{n} ) \rightarrow  q \equiv  (p_{1} \rightarrow q) \land (p_{2} \rightarrow q) \land ...\land  (p_{n} \rightarrow q)$ (分情况证明法)

#### 存在性证明 Existence Proofs

Using **constructive existence proof 构造存在性证明** to establish the truth of $\exists xP( x)$. 

* Establish $P(c) $is true for some $c$ in the domain.
* Then $\exists xP( x)$ is true by Existential Generalization (EG)

Using **nonconstructive existence proof 非构造存在性证明** to establish the truth of  $\exists xP( x)$.  

* Assume no $c$ exists which makes $P(c)$ true and derive a  contradiction 

#### 唯一性证明 Uniqueness Proofs  

To show that a theorem assert the existence of a unique element with  a particular property. 

$$\exists x( P(x) \land  \forall  y ( y≠ x\rightarrow ¬P(y) ) )$$ 

* Existence（存在性）: We show that an element x with the desired  property exists. 
* Uniqueness（唯一性） : We show that if $y≠x$, then y does not have the  desired property. Or, we can show that if $x$ and $y$ both have the  desired property ,then $x=y$.

#### 反例证明 Disproof by Counterexample

Using the method of **disproof by counterexample** to establish that $¬\forall xP(x)$ is true.  

* To construct a $c$ such that $P(c)$ is false. 
* Recall:    $¬\forall xP(x ) ⇔ \exists x¬ P(x)$

#### Nonexistence Proofs 

To establish that $¬\exists xP( x)$ is true .  

* Use a proof by contradiction by assuming there is a $c$ which makes $P(c)$ true . 
* Recall: $¬ \exists x P(x) ⇔ \forall  x ¬ P(x )$

### 2. Proof Strategy

* **Forward reasoning**: Using premises, together with axioms and known theorems to lead to the conclusion.  
* **Backward reasoning**: To reason backward to prove a statement q, we find a statement p that we can prove with the property that $p\rightarrow q$.