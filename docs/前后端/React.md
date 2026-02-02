# React

## 一、React 与 JSX

- 组件化构建 (Component-Based Architecture):

   React 的核心思想是将用户界面拆分成一系列独立、可复用的组件。每个组件负责渲染 UI 的一部分，并管理自身的状态和逻辑。组件可以是简单的函数，也可以是更复杂的类。官方推荐使用函数组件配合 Hooks。

  - **组件命名:** 组件名称必须以**大写字母开头** (例如 `MyComponent`)，以便 React 将其与原生 HTML 标签 (例如 `div`) 区分开来。
  - **可复用性与组合:** 组件的设计强调可复用性。简单的组件可以组合成更复杂的组件，最终构成整个应用程序的 UI。

- JSX (JavaScript XML):

  - **语法扩展:** JSX 是一种 JavaScript 的语法扩展，它允许开发者在 JavaScript 代码中直接书写类似 HTML 的标记结构。这使得描述 UI 结构更加直观和声明式。
  - **非必需但推荐:** 虽然 JSX 不是使用 React 的强制要求（可以使用 `React.createElement`），但它极大地提高了开发效率和代码可读性。
  - **编译:** JSX 最终会被 Babel 等编译器转换为普通的 JavaScript 函数调用（`React.createElement`），浏览器本身并不直接理解 JSX。
  - **JavaScript 表达式嵌入:** 在 JSX 中，可以使用花括号 `{}` 来嵌入任何有效的 JavaScript 表达式，如变量、函数调用、算术运算等。例如：`<h1>Hello, {user.name}</h1>`。
  - **属性:** JSX 元素的属性类似于 HTML 属性，但命名上遵循驼峰命名法 (camelCase)，例如 `className` 对应 HTML 的 `class`，`onClick` 对应 `onclick`。
  - **闭合标签:** JSX 标签必须闭合，对于没有子元素的标签，可以使用自闭合语法，例如 `< img / >`、`< br / >`。
  - **Fragments (`<  >...< / >`):** 如果一个组件需要返回多个顶级元素，可以使用 `React.Fragment` 或其简写语法 `<  >...< / >` 来包裹它们，避免添加不必要的父 `div`。

## 二、组件

### 函数组件 (Functional Components)

- **简洁性:** 本质上是接受 `props` 对象作为参数并返回 React 元素的 JavaScript 函数。

- **无状态与有状态:** 最初，函数组件被认为是无状态的。但通过 **Hooks** (如 `useState`, `useEffect`)，函数组件现在可以拥有和管理自身状态及副作用。

  ```javascript
  function Welcome(props) {
    return <h1>Hello, {props.name}</h1>;
  }
  ```

### 类组件 (Class Components)

- **ES6 类:** 使用 ES6 的 `class` 语法定义，继承自 `React.Component`。

- **`render()` 方法:** 必须实现一个 `render()` 方法，该方法返回 React 元素。

- **`this.props` 和 `this.state`:** 通过 `this.props` 访问传入的属性，通过 `this.state` 管理内部状态。

- **生命周期方法:** 拥有如 `componentDidMount`, `componentDidUpdate`, `componentWillUnmount` 等生命周期方法，用于在组件的不同阶段执行代码。

  ```javascript
  import React from 'react';
  
  class Welcome extends React.Component {
    render() {
      return <h1>Hello, {this.props.name}</h1>;
    }
  }
  ```

## 三、Props (属性)

- **数据传递:** Props (properties 的缩写) 是组件之间传递数据的主要方式，通常是从父组件传递到子组件。
- **只读性 (Read-Only):** 组件接收到的 `props` 是**只读的**。子组件不应该直接修改其接收到的 `props`。这种单向数据流使得应用状态更易于理解和维护。
- **传递任意数据:** `props` 可以是任何 JavaScript 类型，包括字符串、数字、布尔值、数组、对象，甚至函数。
- **`children` Prop:** 一个特殊的 prop，代表组件标签之间的内容。例如，在 `<MyComponent>Hello</MyComponent>` 中，"Hello" 会作为 `props.children` 传递给 `MyComponent`。

## 四、State (状态)

- **组件内部数据:** State 是组件内部私有的数据，用于控制组件的行为和渲染。当 state 发生变化时，React 会自动重新渲染组件以反映这些变化。
- **可变性:与 props 不同，state 是可变的**，并且由组件自身管理。
- `useState` Hook (函数组件):
  - 是函数组件中管理状态的主要方式。
  - 调用 `useState` 会返回一个包含当前状态值和一个更新该状态值的函数的数组。
  - 例如: `const [count, setCount] = useState(0);`
  - 更新状态时，应该使用 `setCount` 函数，而不是直接修改 `count`。React 会确保在状态更新后重新渲染组件。
- `this.state` 和 `this.setState()` (类组件):
  - 在类组件的构造函数中初始化 `this.state` (一个对象)。
  - 使用 `this.setState()` 方法来更新状态。`setState()` 会将更新合并到现有状态，并触发组件的重新渲染。直接修改 `this.state` 

## 五、Props vs. State 详细对比

| **特性**     | **Props**                                                    | **State**                                                    |
| ------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| **数据来源** | 由父组件传入                                                 | 组件内部定义和管理                                           |
| **可变性**   | 只读 (Immutable)，子组件不能直接修改                         | 可变 (Mutable)，通过特定函数 (如 `setState` 或 `useState` 返回的更新函数) 修改 |
| **所有权**   | 归父组件所有                                                 | 归组件自身所有                                               |
| **用途**     | 从父组件向子组件传递数据和配置                               | 管理组件内部会随时间变化的数据，控制组件行为和渲染           |
| **数据流**   | 单向数据流 (父 -> 子)                                        | 通常是组件内部的，但可以通过回调函数影响父组件状态（状态提升） |
| **访问方式** | 函数组件: `props.propertyName`&lt;br>类组件: `this.props.propertyName` | 函数组件: `stateVariable`&lt;br>类组件: `this.state.stateName` |
| **更新方式** | 由父组件重新传递新的 props 值                                | 函数组件: `setStateFunction(newValue)`&lt;br>类组件: `this.setState({ stateName: newValue })` |

**核心原则:**

- 如果一个组件需要根据某些数据来渲染，并且这些数据会随着时间或用户交互而改变，那么这些数据应该存储在 **state** 中。
- 如果一个组件需要从其父组件接收数据来配置其行为或显示内容，那么这些数据应该通过 **props** 传递。
- "状态提升 (Lifting State Up)" 是一种常见模式：当多个子组件需要共享相同的变化数据时，将该 state 提升到它们最近的共同父组件中，然后通过 props 将 state 和更新 state 的函数传递给子组件。

## 六、React Hooks

Hooks 是 React 16.8 版本引入的新特性，它允许你在不编写 class 的情况下使用 state 以及其他的 React 特性。

- 动机:

  - 解决类组件中 `this` 的指向问题。
  - 更好地复用状态逻辑（自定义 Hooks）。
  - 使组件逻辑更扁平化，避免嵌套地狱。

- 基本规则:

  - **只能在函数组件的顶层调用 Hooks:** 不要在循环、条件判断或嵌套函数中调用 Hooks。这能确保 Hooks 在每次渲染时都以相同的顺序被调用。
  - **只能在 React 函数组件或自定义 Hooks 中调用 Hooks:** 不要在普通的 JavaScript 函数中调用 Hooks。

- 常用内置 Hooks:

  - **`useState`:** 如前所述，用于在函数组件中添加和管理 state。

  - `useEffect`:

     用于处理副作用 (side effects)，如数据获取、订阅、手动更改 DOM 等。它类似于类组件中的 `componentDidMount`、`componentDidUpdate` 和 `componentWillUnmount` 的组合。

    - 可以接收一个可选的依赖项数组作为第二个参数。如果依赖项数组中的任何值发生变化，`useEffect` 中的函数就会重新执行。如果传入空数组 `[]`，则 effect 只会在组件挂载和卸载时执行一次。如果不传第二个参数，则 effect 会在每次渲染后执行。

  - **`useContext`:** 用于在组件树中订阅 React context，避免通过 props 逐层传递数据。

  - **`useReducer`:** `useState` 的替代方案，通常用于管理更复杂的状态逻辑，或者当下一个状态依赖于前一个状态时。它接受一个 reducer 函数和初始状态，返回当前状态和 `dispatch` 函数。

  - **`useCallback`:** 返回一个 memoized 回调函数。只有当它的某个依赖项改变时，才会重新创建这个回调函数。用于优化，避免不必要的子组件重渲染。

  - **`useMemo`:** 返回一个 memoized 值。只有当它的某个依赖项改变时，才会重新计算这个值。用于优化昂贵的计算。

  - **`useRef`:** 返回一个可变的 ref 对象，其 `.current` 属性被初始化为传递的参数（initialValue）。`useRef` 创建的 ref 对象在组件的整个生命周期内保持不变。常用于访问 DOM 元素或在多次渲染之间持久化任何可变值。

- 自定义 Hooks (Custom Hooks):

  - 允许你将组件逻辑提取到可重用的函数中。
  - 自定义 Hook 是一个以 "use" 开头的 JavaScript 函数，内部可以调用其他 Hooks。
  - 例如，你可以创建一个 `useFormInput` Hook 来处理表单输入的逻辑。

## **七、条件渲染**

React 中没有特殊的条件渲染语法，而是直接使用 JavaScript 的条件语句。

- `if` **语句:**

  ```javascript
  function Greeting(props) {
    const isLoggedIn = props.isLoggedIn;
    if (isLoggedIn) {
      return <UserGreeting />;
    }
    return <GuestGreeting />;
  }
  ```

- 逻辑与运算**符** `&&`**:**

   如果条件为真，则渲染 `&&` 右侧的表达式；否则不渲染。

  ```javascript
  function Mailbox(props) {
    const unreadMessages = props.unreadMessages;
    return (
      <div>
        <h1>Hello!</h1>
        {unreadMessages.length > 0 &&
          <h2>
            You have {unreadMessages.length} unread messages.
          </h2>
        }
      </div>
    );
  }
  ```

- **三元运算符** `condition ? trueExpression : falseExpression`**:**

  ```javascript
  render() {
    const isLoggedIn = this.state.isLoggedIn;
    return (
      <div>
        {isLoggedIn ? (
          <LogoutButton onClick={this.handleLogoutClick} />
        ) : (
          <LoginButton onClick={this.handleLoginClick} />
        )}
      </div>
    );
  }
  ```

- **阻止组件渲染:** 在极少数情况下，你可能希望组件隐藏自身，即使它是由另一个组件渲染的。为此，你可以让 `render` 方法返回 `null`。

## **八、列表与 Keys**

- **使用** `map()` **渲染列表:**

   通常使用 JavaScript 的 `map()` 方法来遍历数组并为每个项渲染一个 React 元素或组件。

  ```JavaScript
  function NumberList(props) {
    const numbers = props.numbers;
    const listItems = numbers.map((number) =>
      <li key={number.toString()}> // Key 很重要!
        {number}
      </li>
    );
    return (
      <ul>{listItems}</ul>
    );
  }
  ```

- Keys:

  - `key` 是一个特殊的字符串属性，当创建元素列表时需要包含它。
  - Keys 帮助 React 识别哪些项已更改、添加或删除。
  - **稳定性与唯一性:** key 应该在兄弟节点之间是唯一的，并且应该是稳定的（不应在后续渲染中改变）。通常使用数据中的唯一 ID 作为 key。
  - **作用范围:** Key 只需要在当前列表的兄弟节点中唯一，不需要全局唯一。
  - **不建议使用索引作为 key:** 如果列表的顺序可能会改变，或者项会被插入/删除，使用数组索引作为 key 可能会导致性能问题和状态混乱。

## 九、样式

- `className`: 使用 `className` 属性来指定 CSS 类。

  ```javascript
  <div className="my-class">...</div>
  ```

- **CSS 文件:** 可以在单独的 CSS 文件中编写样式，然后像在普通 HTML 中一样引入。

- 内联样式 (Inline Styles):

  - 内联样式是通过一个 JavaScript 对象传递给 `style` 属性的。
  - 对象的键是 CSS 属性的驼峰式命名 (例如 `backgroundColor` 而不是 `background-color`)。
  - 值通常是字符串，但对于某些数值属性（如 `fontSize`, `width`, `height`），React 会自动添加 "px" 后缀（除非你明确指定单位）。

  ```javascript
  const divStyle = {
    color: 'blue',
    backgroundImage: 'url(' + imgUrl + ')',
    WebkitTransition: 'all', // 支持浏览器前缀
    msTransition: 'all' // 支持浏览器前缀
  };
  
  function HelloWorldComponent() {
    return <div style={divStyle}>Hello World!</div>;
  }
  ```

- **CSS Modules:** 一种流行的 CSS 作用域解决方案，确保样式只应用于特定组件，避免全局样式冲突。

- **CSS-in-JS 库:** 例如 Styled Components, Emotion 等，允许你在 JavaScript 文件中直接编写 CSS，提供更强大的动态样式和主题化能力。