(() => {
  "use strict";

  const MATHJAX_URL = "https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js";
  const MERMAID_URL = "https://unpkg.com/mermaid/dist/mermaid.min.js";

  const scriptPromises = new Map();
  let mathJaxRender = Promise.resolve();
  let mermaidRender = Promise.resolve();

  function loadScript(src) {
    if (scriptPromises.has(src)) return scriptPromises.get(src);

    const existing = document.querySelector(`script[src="${src}"]`);
    const promise = existing
      ? Promise.resolve()
      : new Promise((resolve, reject) => {
          const script = document.createElement("script");
          script.src = src;
          script.async = true;
          script.onload = resolve;
          script.onerror = () => reject(new Error(`Failed to load ${src}`));
          document.head.appendChild(script);
        });

    scriptPromises.set(src, promise);
    return promise;
  }

  function renderMath() {
    const nodes = [...document.querySelectorAll(".arithmatex:not([data-rendered]):not([data-rendering])")];
    if (!nodes.length) return;
    nodes.forEach(node => { node.dataset.rendering = "mathjax"; });

    if (!window.MathJax) {
      window.MathJax = {
        tex: {
          inlineMath: [["$", "$"], ["\\(", "\\)"]],
          displayMath: [["$$", "$$"], ["\\[", "\\]"]],
          processEscapes: true,
          processEnvironments: true
        },
        options: {
          ignoreHtmlClass: ".*",
          processHtmlClass: "arithmatex.*"
        }
      };
    }

    mathJaxRender = mathJaxRender
      .then(() => loadScript(MATHJAX_URL))
      .then(() => window.MathJax.startup.promise)
      .then(() => window.MathJax.typesetPromise(nodes))
      .then(() => nodes.forEach(node => {
        node.dataset.rendered = "mathjax";
        delete node.dataset.rendering;
      }))
      .catch(error => {
        nodes.forEach(node => { delete node.dataset.rendering; });
        console.error("MathJax rendering failed:", error);
      });
  }

  function renderMermaid() {
    const nodes = [...document.querySelectorAll(".mermaid:not([data-processed]):not([data-rendering])")];
    if (!nodes.length) return;
    nodes.forEach(node => { node.dataset.rendering = "mermaid"; });

    mermaidRender = mermaidRender
      .then(() => loadScript(MERMAID_URL))
      .then(() => {
        window.mermaid.initialize({ startOnLoad: false });
        return window.mermaid.run({ nodes });
      })
      .then(() => nodes.forEach(node => { delete node.dataset.rendering; }))
      .catch(error => {
        nodes.forEach(node => { delete node.dataset.rendering; });
        console.error("Mermaid rendering failed:", error);
      });
  }

  function renderPage() {
    renderMath();
    renderMermaid();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", renderPage, { once: true });
  } else {
    renderPage();
  }

  if (typeof document$ !== "undefined") {
    document$.subscribe(renderPage);
  }
})();
