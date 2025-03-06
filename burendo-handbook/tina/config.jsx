import { defineConfig, LocalAuthProvider } from "tinacms";
import {
  TinaUserCollection,
  UsernamePasswordAuthJSProvider,
} from 'tinacms-authjs/dist/tinacms'

// Your hosting provider likely exposes this as an environment variable
const branch =
  process.env.GITHUB_BRANCH ||
  process.env.HEAD ||
  "main";

const isLocal = process.env.TINA_PUBLIC_IS_LOCAL === "true";

const docusaurusDate = (val) => {
  let ye = new Intl.DateTimeFormat("en", {
    year: "numeric",
  }).format(val);
  let mo = new Intl.DateTimeFormat("en", {
    month: "2-digit",
  }).format(val);
  let da = new Intl.DateTimeFormat("en", {
    day: "2-digit",
  }).format(val);
  return `${ye}-${mo}-${da}`;
};

const blogsCollection = {
  name: "blog",
  label: "Blog",
  path: "blog",
  fields: [
    {
      type: "string",
      name: "title",
      label: "Title",
      isTitle: true,
      required: true,
    },
    {
      type: "string",
      name: "description",
      label: "Description",
      required: true,
    },
    {
      type: "string",
      name: "date",
      label: "Date",
      required: false,
      ui: {
        dateFormat: "MMM D, yyyy",
        component: "date",
        parse: (val) => {
          return docusaurusDate(val);
        },
      },
    },
    {
      name: "authors",
      label: "Authors",
      type: "string",
      list: false,
      // ui: {
      //   itemProps: (item) => {
      //     return { label: item?.name };
      //   },
      // },
      // fields: [
      //   {
      //     name: "name",
      //     label: "Name",
      //     type: "string",
      //     isTitle: true,
      //     required: true,
      //   },
      //   {
      //     name: "title",
      //     label: "Title",
      //     type: "string",
      //   },
      //   {
      //     name: "url",
      //     label: "URL",
      //     type: "string",
      //   },
      //   {
      //     name: "email",
      //     label: "Email",
      //     type: "string",
      //   },
      //   {
      //     name: "image_url",
      //     label: "Image URL",
      //     type: "string",
      //   },
      // ],
    },
    {
      type: "image",
      name: "cover_image",
      label: "Cover Image",
      required: false,
    },
    {
      type: "string",
      name: "slug",
      label: "Slug",
      required: false,
    },
    {
      type: "string",
      name: "tags",
      label: "Tags",
      list: true,
      required: false,
      ui: {
        component: "tags",
      },
    },
    {
      type: "rich-text",
      name: "body",
      label: "Body",
      isBody: true,
    },
  ],
}

const docsCollection = {
  name: "docs",
  label: "Docs",
  path: "docs",
  fields: [
    {
      type: "string",
      name: "title",
      label: "Title",
      required: false,
    },
    {
      type: "string",
      name: "description",
      label: "Description",
      required: false,
    },
    {
      type: "number",
      name: "sidebar_position",
      label: "Sidebar Position",
      required: true,
    },
    {
      type: "string",
      name: "slug",
      label: "Slug",
      required: false,
    },
    {
      type: "string",
      name: "pagination_next",
      label: "Next Page",
      required: false,
    },
    {
      type: "string",
      name: "pagination_prev",
      label: "Previous Page",
      required: false,
    },
    {
      type: "string",
      name: "tags",
      label: "Tags",
      list: true,
      required: false,
      ui: {
        component: "tags",
      },
    },
    {
      type: "rich-text",
      name: "body",
      label: "Body",
      isBody: true,
    },
  ],
}

export default defineConfig({
  ...(isLocal? {}: {contentApiUrlOverride: '/api/tina/gql' }),

  branch,
  clientId: process.env.NEXT_PUBLIC_TINA_CLIENT_ID,
  token: process.env.TINA_TOKEN,

  authProvider: isLocal
    ? new LocalAuthProvider()
    : new UsernamePasswordAuthJSProvider(),

  build: {
    outputFolder: "admin",
    publicFolder: "static",
  },

  media: {
    tina: {
      mediaRoot: "img",
      publicFolder: "static",
    },
  },

  // See docs on content modelling for more info on how to setup new content models: https://tina.io/docs/schema/
  schema: {
    collections: [
      TinaUserCollection,
      blogsCollection,
      docsCollection,
    ],
  },
});
