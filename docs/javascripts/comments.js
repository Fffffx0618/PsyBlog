(() => {
  "use strict";

  const siteRoot = new URL("../", document.currentScript.src);

  const theme = () => document.body.dataset.mdColorScheme === "slate"
    ? "github-dark" : "github-light";

  function mountComments() {
    const path = window.location.pathname;
    if (path === siteRoot.pathname || path === `${siteRoot.pathname}index.html`) return;

    const article = document.querySelector(".md-content__inner");
    if (!article || article.querySelector("#comments")) return;

    const section = document.createElement("section");
    section.id = "comments";
    section.setAttribute("aria-label", "评论区");
    const heading = document.createElement("h2");
    heading.textContent = "评论区";
    const description = document.createElement("p");
    description.textContent = "使用 GitHub 登录即可留言，欢迎大家留言～";
    const fallback = document.createElement("a");
    fallback.href = "https://github.com/Fffffx0618/PsyBlog/issues";
    const script = document.createElement("script");
    script.src = "https://utteranc.es/client.js";
    script.setAttribute("repo", "Fffffx0618/PsyBlog");
    script.setAttribute("issue-term", "pathname");
    script.setAttribute("theme", theme());
    script.crossOrigin = "anonymous";
    script.async = true;
    section.append(heading, description, fallback, script);
    article.append(section);
  }

  new MutationObserver(() => {
    const frame = document.querySelector("#comments .utterances-frame");
    frame?.contentWindow?.postMessage({ type: "set-theme", theme: theme() }, "https://utteranc.es");
  }).observe(document.body, { attributes: true, attributeFilter: ["data-md-color-scheme"] });

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", mountComments, { once: true });
  } else {
    mountComments();
  }
  if (typeof document$ !== "undefined") document$.subscribe(mountComments);
})();
