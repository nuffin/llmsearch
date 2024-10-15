import { fixupConfigRules, fixupPluginRules } from '@eslint/compat'
import typescriptEslint from '@typescript-eslint/eslint-plugin'
import prettier from 'eslint-plugin-prettier'
import testingLibrary from 'eslint-plugin-testing-library'
import tsParser from '@typescript-eslint/parser'
import path from 'node:path'
import { fileURLToPath } from 'node:url'
import js from '@eslint/js'
import { FlatCompat } from '@eslint/eslintrc'

const __filename = fileURLToPath(import.meta.url)
const __dirname = path.dirname(__filename)
const compat = new FlatCompat({
  baseDirectory: __dirname,
  recommendedConfig: js.configs.recommended,
  allConfig: js.configs.all,
})

export default [
  ...fixupConfigRules(
    compat.extends(
      'eslint:recommended',
      'plugin:react/recommended',
      'plugin:react-hooks/recommended',
      'plugin:react/jsx-runtime',
      'next/core-web-vitals',
      'next/typescript',
      'plugin:@typescript-eslint/strict',
      'plugin:@typescript-eslint/recommended',
      'plugin:storybook/recommended'
    )
  ),
  {
    plugins: {
      '@typescript-eslint': fixupPluginRules(typescriptEslint),
      prettier,
      'testing-library': testingLibrary,
    },

    languageOptions: {
      parser: tsParser,
      ecmaVersion: 5,
      sourceType: 'script',

      parserOptions: {
        project: './tsconfig.json',
      },
    },

    rules: {
      '@typescript-eslint/consistent-type-imports': 'off',

      '@typescript-eslint/no-unused-vars': [
        'error',
        {
          argsIgnorePattern: '^_',
          varsIgnorePattern: '^_',
        },
      ],

      'no-unused-vars': [
        'error',
        {
          argsIgnorePattern: '^_',
          varsIgnorePattern: '^_',
        },
      ],

      'prettier/prettier': 'off',
      '@next/next/no-img-element': 'off',
      // "@typescript-eslint/no-extra-semi": "warn",
      'no-useless-escape': 'off',
      'no-extra-boolean-cast': 'off',
      'no-constant-condition': 'off',
      // "no-extra-semi": "off",
      '@typescript-eslint/no-unnecessary-condition': 'off',
      'no-restricted-syntax': [
        'error',
        'AwaitExpression > AwaitExpression.argument',
      ],
      '@typescript-eslint/consistent-type-definitions': 'off',
      'import/newline-after-import': 'error',

      'react/jsx-curly-brace-presence': [
        'warn',
        {
          props: 'never',
          children: 'never',
        },
      ],
    },
  },
  ...compat.extends('plugin:testing-library/react').map((config) => ({
    ...config,
    files: ['**/test/**/*.[jt]s?(x)', '**/?(*.)+(spec|test).[jt]s?(x)'],
  })),
]
