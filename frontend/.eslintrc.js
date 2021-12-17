/**
 * @file eslint config
 * @author
 */

module.exports = {
    root: true,
    parser: 'vue-eslint-parser',
    parserOptions: {
        sourceType: 'module'
    },
    extends: [
        'plugin:vue/vue3-strongly-recommended'
    ],
    env: {
        browser: true,
        es6: true
    },
    plugins: ['vue'],
    rules: {
        'vue/html-indent': ['error', 4],
        'vue/html-closing-bracket-newline': 'off',
        'vue/max-attributes-per-line': 'off',
        'vue/v-on-event-hyphenation': 'off',
        'vue/script-indent': ['error', 4, { 'baseIndent': 1, 'switchCase': 1 }],
        'vue/html-quotes': ['error', 'double', { 'avoidEscape': false }],
        'object-curly-spacing': ['error', 'always'],
        'vue/require-valid-default-prop': 'off',
        'quotes': ['error', 'single'],
        'vue/multi-word-component-names': 'off',
        'semi': ['error', 'never'],
        'vue/comment-directive': 'off',
        'vue/object-curly-spacing': ['error', 'always'],
        'vue/no-unused-properties': ['error'],
        'vue/no-unused-components': ['error'],
        'vue/no-unused-vars': ['error'],
        'vue/no-unused-refs': ['error'],
        'vue/no-side-effects-in-computed-properties': 'off'
    }
}