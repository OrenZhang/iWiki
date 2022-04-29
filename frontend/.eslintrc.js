/**
 * @file eslint config
 * @author
 */

module.exports = {
  root: true,
  parser: 'vue-eslint-parser',
  parserOptions: {
    ecmaVersion: 2021,
    sourceType: 'module',
  },
  env: {
    browser: true,
    es6: true,
  },
  extends: ['plugin:vue/vue3-strongly-recommended', '@tencent/eslint-config-tencent'],
  rules: {
    'vue/no-side-effects-in-computed-properties': 'off',
  },
};
