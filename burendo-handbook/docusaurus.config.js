// @ts-check
// Note: type annotations allow type checking and IDEs autocompletion

const lightCodeTheme = require('prism-react-renderer').themes.github;
const darkCodeTheme = require('prism-react-renderer').themes.dracula;
require("dotenv").config();
console.log(process.env);

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: "The Burendo Handbook",
  tagline: "Together, it's possible",
  url: "https://handbook.burendo.com",
  baseUrl: "/",
  staticDirectories: ['static', 'docs'],
  onBrokenLinks: "ignore",
  onBrokenMarkdownLinks: "warn",
  favicon: "img/burendo_logo.png",
  plugins: [
    [
      require.resolve("@easyops-cn/docusaurus-search-local"),
      ({
        hashed: true,
        indexDocs: true,
        indexBlog: true,
        language: ["en"],
      }),
    ],
  ],

  // GitHub pages deployment config.
  // If you aren't using GitHub pages, you don't need these.
  organizationName: "burendouk", // Usually your GitHub org/user name.
  projectName: "burendo-handbook", // Usually your repo name.

  // Even if you don't use internalization, you can use this field to set useful
  // metadata like html lang. For example, if your site is Chinese, you may want
  // to replace "en" with "zh-Hans".
  i18n: {
    defaultLocale: "en",
    locales: ["en"],
  },

  presets: [
    [
      "classic",
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          routeBasePath: "/",
          sidebarPath: require.resolve("./sidebars.js"),
          // Please change this to your repo.
          // Remove this to remove the "edit this page" links.
          // editUrl:
          //   "https://github.com/BurendoUK/burendo-handbook-public/blob/main/",
        },
        blog: {
          blogTitle: "Burendo blog!",
          blogDescription: "Thoughts from our Burendoers",
          postsPerPage: "ALL",
          showReadingTime: true,
          feedOptions: {
            type: "all",
            title: "Burendo blog",
            description: "Blogs from our Burendoers",
            copyright: "2023 @ Burendo Ltd",
          },
        },
        theme: {
          customCss: require.resolve("./src/css/custom.css"),
        },
        gtag: {
          trackingID: "G-6SG9CBCS3W",
          anonymizeIP: true,
        },
      }),
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      image: "img/burendo_logo_horizontal.png",
      colorMode: {
        defaultMode: "dark",
        disableSwitch: false,
        respectPrefersColorScheme: false,
      },
      navbar: {
        hideOnScroll: true,
        title: "The Burendo Handbook",
        logo: {
          alt: "Burendo Logo",
          src: "img/burendo_logo.png",
        },
        items: [
          {
            to: "blog",
            label: "Blog",
            position: "right",
          },
        ],
      },
      footer: {
        style: "dark",
        links: [
          {
            title: "Community",
            items: [
              {
                label: "Burendo Website",
                href: "https://burendo.com",
              },
              {
                label: "LinkedIn",
                href: "https://www.linkedin.com/company/burendo-consulting/",
              },
              {
                label: "Twitter",
                href: "https://twitter.com/burendoUK",
              },
            ],
          },
          {
            title: "More",
            items: [
              {
                label: "GitHub Org",
                href: "https://github.com/BurendoUK",
              },
              {
                label: "GitHub Repo",
                href: "https://github.com/BurendoUK/burendo-handbook-infrastructure",
              },
            ],
          },
        ],
        copyright: `Copyright © ${new Date().getFullYear()} Burendo Limited. Built with Docusaurus.`,
      },
      prism: {
        theme: lightCodeTheme,
        darkTheme: darkCodeTheme,
      },
    }),

  markdown: {
    mermaid: true,
  },

  themes: ["@docusaurus/theme-mermaid"],
};

module.exports = config;
