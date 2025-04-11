# Contributing Guidelines

Thank you for your interest in contributing to the **ODR Rescue Boxes** project! Please follow these guidelines to ensure smooth collaboration.

## Branch Naming Conventions

When creating a new branch, follow these naming conventions:

- `feat/<branch-name>` → For new features.
- `refactor/<branch-name>` → For code refactoring without adding new features.
- `bugFix/<branch-name>` → For fixing bugs.
- `hotFix/<branch-name>` → For urgent and critical fixes.
- `docs/<branch-name>` → For documentation updates.

## Coding Standards

### Buttons and Typography

- Define buttons in `src/styles/buttons`.
- Import typography elements (`H1, H2, ..., H6, P1, P2, Section`) from `src/styles/typography`.
- Always import typography as:
  ```tsx
  import * as T from 'src/styles/typography'
  ```
  and use it like:
  ```tsx
  <T.H1>Heading</T.H1>
  ```

### Page Structure

- Wrap every page with `PageLoadingAnimation` from `src/styles/animations`.
- Wrap the whole application with `RootStructure` from `src/styles/templates` to handle client providers (e.g., React Query). This cannot be done in `layout.tsx` as it is server-rendered.
- Use `Layout` from `src/styles/template/layout` to define maximum width for pages.

## Commit Message Guidelines

Always write meaningful commit messages. Follow this format:

```
[Type]: Short description

Example:
feat: Add new search functionality
bugFix: Fix broken navigation links
```

## Icons

- **Do not use any icon libraries**.
- Use **Google Icons** instead:

  1. Copy the SVG code from Google Icons.
  2. Save it in `src/styles/icons/`.
  3. Export it with a meaningful name based on the website icon name.

  Example:

  ```tsx
  export const KeyboardArrowUpIcon: React.FC<IconProps> = ({
    color,
    size = 24,
    className,
  }) => (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      viewBox="0 -960 960 960"
      width={size}
      height={size}
      className={`fill-current ${className}`}
      fill={color || defaultColor}
    >
      <path d="M480-528 296-344l-56-56 240-240 240 240-56 56-184-184Z" />
    </svg>
  )
  ```

## Component Organization

- If a component is used **only in one page**, keep it inside the same file.
- If a component is used **two or more times**, create a separate component file.

## ESLint & Prettier

- **Do not modify ESLint or Prettier settings**.
- **Strictly avoid using `@ts-ignore` or ESLint ignore rules**.

## Tailwind CSS Usage

- **Do not use inline Tailwind styles like `bg-[#afe34]`**.
- Define custom colors in Tailwind with a prefix like `c-yellow` for `custom-yellow`.

---

By following these guidelines, we ensure consistency and maintainability across the project. Happy coding! 🚀
