// @ts-check
// Note: type annotations allow type checking and IDEs autocompletion

const lightCodeTheme = require("prism-react-renderer/themes/github");
const darkCodeTheme = require("prism-react-renderer/themes/dracula");

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: "Burendo Handbook",
  tagline: "Together, it's possible",
  url: "https://handbook.burendo.com",
  baseUrl: "/",
  onBrokenLinks: "ignore",
  onBrokenMarkdownLinks: "warn",
  favicon: "img/favicon.ico",

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
        blog: false,
        theme: {
          customCss: require.resolve("./src/css/custom.css"),
        },
      }),
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      navbar: {
        title: "Burendo Handbook",
        logo: {
          alt: "Burendo Logo",
          src: "img/burendo_outline.png",
        },
        items: [
          {
            type: "doc",
            docId: "intro",
            position: "left",
            label: "Handbook",
          },
          {
            href: "https://github.com/BurendoUK/burendo-handbook-infrastructure",
            label: "GitHub",
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
                label: "GitHub",
                href: "https://github.com/BurendoUK",
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
};

module.exports = config;
