window.MathJax = {
  tex: {
    inlineMath: [["$", "$"], ["\\(", "\\)"]],
    displayMath: [["$$", "$$"], ["\\[", "\\]"]],
    processEscapes: true,
    processEnvironments: true
  },
  options: {
    ignoreHtmlClass: ".*",
    processHtmlClass: "arithmatex.*"  // ← 关键修复：匹配所有 arithmatex 开头的类
  }
};

// 初始化 MathJax
document.addEventListener("DOMContentLoaded", () => {
  if (typeof MathJax !== "undefined") {
    MathJax.startup.promise = MathJax.startup.promise
      .then(() => MathJax.typesetPromise())
      .catch(err => console.log("MathJax typeset error:", err));
  }
});

// Material 主题集成：页面切换时重新渲染
if (typeof document$ !== "undefined") {
  document$.subscribe(() => {
    if (typeof MathJax !== "undefined") {
      MathJax.startup.promise = MathJax.startup.promise
        .then(() => MathJax.typesetPromise())
        .catch(err => console.log("MathJax typeset error:", err));
    }
  });
}