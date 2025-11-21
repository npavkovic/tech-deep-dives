const rssPlugin = require("@11ty/eleventy-plugin-rss");
const markdownIt = require("markdown-it");
const markdownItAnchor = require("markdown-it-anchor");
const markdownItTOC = require("markdown-it-toc-done-right");

module.exports = function(eleventyConfig) {
  eleventyConfig.addPlugin(rssPlugin);

  // Configure markdown with TOC support
  const markdownLibrary = markdownIt({
    html: true,
    linkify: true,
    typographer: true
  })
    .use(markdownItAnchor, {
      permalink: markdownItAnchor.permalink.ariaHidden({
        placement: 'after',
        class: 'header-anchor',
        symbol: '#',
        ariaHidden: false
      }),
      level: [2, 3],
      slugify: eleventyConfig.getFilter("slugify")
    })
    .use(markdownItTOC, {
      containerClass: "toc",
      listType: "ul",
      level: [2, 3]
    });

  eleventyConfig.setLibrary("md", markdownLibrary);

  // Copy audio files and CSS to output
  eleventyConfig.addPassthroughCopy("audio");
  eleventyConfig.addPassthroughCopy("css");

  // Custom filter to format dates (works with both Date objects and strings)
  eleventyConfig.addFilter("readableDate", (dateObj) => {
    const date = typeof dateObj === 'string' ? new Date(dateObj) : dateObj;
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  });

  // Custom filter for RFC 3339 dates (works with both Date objects and strings)
  eleventyConfig.addFilter("isoDate", (dateObj) => {
    const date = typeof dateObj === 'string' ? new Date(dateObj) : dateObj;
    return date.toISOString();
  });

  // Sort guides by date, newest first
  eleventyConfig.addCollection("guides", function(collectionApi) {
    return collectionApi.getFilteredByGlob("guides/*.md").sort((a, b) => {
      const dateA = typeof a.date === 'string' ? new Date(a.date) : a.date;
      const dateB = typeof b.date === 'string' ? new Date(b.date) : b.date;
      return dateB - dateA;
    });
  });

  return {
    dir: {
      input: ".",
      output: "_site",
      includes: "_includes"
    }
  };
};
