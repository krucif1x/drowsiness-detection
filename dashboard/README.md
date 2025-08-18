# Drowsiness Detection React Dashboard
This is folder for holding the code for the drowsiness detection project internal dashbord using React v19. The dashboard are getting the video stream of the data result from the Mediapipe calculation and other things such as using Realtime Facial Metrics and some event data

## Build
To build the dashboard, run the following commands:
```bash
npm install
npm run build
```
This will compile the React code and generate the production-ready files in the `dist/` directory

## Run
To run the development server locally:
```bash
npm install
npm run dev
```
This will start the dashboard on http://localhost:3000 by default. You can access it through your browser to see the live feed and metrics.

You can also run the output of the build directly by using a static file server. For example:
```bash
npx serve -s build
```

This will serve the contents of the dist/ folder on a local server (usually at http://localhost:3000), allowing you to preview the production build without deploying it.

## Expanding the ESLint configuration

If you are developing a production application, we recommend updating the configuration to enable type-aware lint rules:

```js
export default tseslint.config({
  extends: [
    // Remove ...tseslint.configs.recommended and replace with this
    ...tseslint.configs.recommendedTypeChecked,
    // Alternatively, use this for stricter rules
    ...tseslint.configs.strictTypeChecked,
    // Optionally, add this for stylistic rules
    ...tseslint.configs.stylisticTypeChecked,
  ],
  languageOptions: {
    // other options...
    parserOptions: {
      project: ['./tsconfig.node.json', './tsconfig.app.json'],
      tsconfigRootDir: import.meta.dirname,
    },
  },
})
```

You can also install [eslint-plugin-react-x](https://github.com/Rel1cx/eslint-react/tree/main/packages/plugins/eslint-plugin-react-x) and [eslint-plugin-react-dom](https://github.com/Rel1cx/eslint-react/tree/main/packages/plugins/eslint-plugin-react-dom) for React-specific lint rules:

```js
// eslint.config.js
import reactX from 'eslint-plugin-react-x'
import reactDom from 'eslint-plugin-react-dom'

export default tseslint.config({
  plugins: {
    // Add the react-x and react-dom plugins
    'react-x': reactX,
    'react-dom': reactDom,
  },
  rules: {
    // other rules...
    // Enable its recommended typescript rules
    ...reactX.configs['recommended-typescript'].rules,
    ...reactDom.configs.recommended.rules,
  },
})
```
