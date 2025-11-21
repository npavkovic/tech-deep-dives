const rssPlugin = require("@11ty/eleventy-plugin-rss");

module.exports = function(eleventyConfig) {
  eleventyConfig.addPlugin(rssPlugin);

  // Copy audio files and CSS to output
  eleventyConfig.addPassthroughCopy("audio");
  eleventyConfig.addPassthroughCopy("css");

  // Sort guides by date, newest first
  eleventyConfig.addCollection("guides", function(collectionApi) {
    return collectionApi.getFilteredByGlob("guides/*.md").sort((a, b) => {
      return b.date - a.date;
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
