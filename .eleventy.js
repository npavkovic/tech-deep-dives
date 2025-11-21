const rssPlugin = require("@11ty/eleventy-plugin-rss");

module.exports = function(eleventyConfig) {
  eleventyConfig.addPlugin(rssPlugin);

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
