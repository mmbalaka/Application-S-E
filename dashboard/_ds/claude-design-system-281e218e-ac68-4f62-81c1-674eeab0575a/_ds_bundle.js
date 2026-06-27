/* @ds-bundle: {"format":3,"namespace":"ClaudeDesignSystem_281e21","components":[{"name":"Button","sourcePath":"components/buttons/Button.jsx"},{"name":"IconButton","sourcePath":"components/buttons/IconButton.jsx"},{"name":"Badge","sourcePath":"components/feedback/Badge.jsx"},{"name":"Input","sourcePath":"components/forms/Input.jsx"},{"name":"CategoryTabs","sourcePath":"components/navigation/CategoryTabs.jsx"},{"name":"Card","sourcePath":"components/surfaces/Card.jsx"}],"sourceHashes":{"components/buttons/Button.jsx":"91914fea71d9","components/buttons/IconButton.jsx":"f1df1255470c","components/feedback/Badge.jsx":"221e7b201615","components/forms/Input.jsx":"25e06b6a766e","components/navigation/CategoryTabs.jsx":"e6bffe5c51ff","components/surfaces/Card.jsx":"c4344c9ece5a","ui_kits/marketing/CTASection.jsx":"0fe5f51386b3","ui_kits/marketing/Features.jsx":"86edd07d2f97","ui_kits/marketing/Footer.jsx":"88f9ceef02d7","ui_kits/marketing/Hero.jsx":"23b31e35d6fc","ui_kits/marketing/ProductShowcase.jsx":"93f54006aef5","ui_kits/marketing/TopNav.jsx":"1623510cb0bd"},"inlinedExternals":[],"unexposedExports":[]} */

(() => {

const __ds_ns = (window.ClaudeDesignSystem_281e21 = window.ClaudeDesignSystem_281e21 || {});

const __ds_scope = {};

(__ds_ns.__errors = __ds_ns.__errors || []);

// components/buttons/Button.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/**
 * Button — the Claude primary action control.
 * Coral primary CTA, cream secondary, on-dark secondary, text link, sizes.
 */
function Button({
  children,
  variant = 'primary',
  size = 'md',
  disabled = false,
  iconLeft = null,
  iconRight = null,
  onClick,
  type = 'button',
  style = {},
  ...rest
}) {
  const sizes = {
    sm: {
      height: 32,
      padding: '0 14px',
      fontSize: 13
    },
    md: {
      height: 40,
      padding: '0 20px',
      fontSize: 14
    },
    lg: {
      height: 48,
      padding: '0 26px',
      fontSize: 15
    }
  };
  const s = sizes[size] || sizes.md;
  const variants = {
    primary: {
      background: disabled ? 'var(--primary-disabled)' : 'var(--primary)',
      color: disabled ? 'var(--muted)' : 'var(--on-primary)',
      border: '1px solid transparent'
    },
    secondary: {
      background: 'var(--canvas)',
      color: 'var(--ink)',
      border: '1px solid var(--hairline)'
    },
    'secondary-on-dark': {
      background: 'var(--surface-dark-elevated)',
      color: 'var(--on-dark)',
      border: '1px solid transparent'
    },
    'on-coral': {
      background: 'var(--canvas)',
      color: 'var(--ink)',
      border: '1px solid transparent'
    },
    text: {
      background: 'transparent',
      color: 'var(--ink)',
      border: '1px solid transparent',
      padding: '0 4px'
    }
  };
  const v = variants[variant] || variants.primary;
  return /*#__PURE__*/React.createElement("button", _extends({
    type: type,
    disabled: disabled,
    onClick: onClick,
    style: {
      display: 'inline-flex',
      alignItems: 'center',
      justifyContent: 'center',
      gap: 8,
      height: s.height,
      padding: variant === 'text' ? v.padding : s.padding,
      fontSize: s.fontSize,
      fontFamily: 'var(--font-body)',
      fontWeight: 500,
      lineHeight: 1,
      letterSpacing: 0,
      borderRadius: 'var(--radius-md)',
      cursor: disabled ? 'not-allowed' : 'pointer',
      transition: 'background var(--duration-fast) var(--ease-standard)',
      whiteSpace: 'nowrap',
      ...v,
      ...style
    },
    onMouseDown: e => {
      if (!disabled && variant === 'primary') e.currentTarget.style.background = 'var(--primary-active)';
    },
    onMouseUp: e => {
      if (!disabled && variant === 'primary') e.currentTarget.style.background = 'var(--primary)';
    },
    onMouseLeave: e => {
      if (!disabled && variant === 'primary') e.currentTarget.style.background = 'var(--primary)';
    }
  }, rest), iconLeft, children, iconRight);
}
Object.assign(__ds_scope, { Button });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/buttons/Button.jsx", error: String((e && e.message) || e) }); }

// components/buttons/IconButton.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/**
 * IconButton — 36px circular icon button. Carousel arrows, share, "view more".
 */
function IconButton({
  children,
  variant = 'cream',
  size = 36,
  ariaLabel,
  onClick,
  disabled = false,
  style = {},
  ...rest
}) {
  const variants = {
    cream: {
      background: 'var(--canvas)',
      color: 'var(--ink)',
      border: '1px solid var(--hairline)'
    },
    dark: {
      background: 'var(--surface-dark-elevated)',
      color: 'var(--on-dark)',
      border: '1px solid transparent'
    },
    coral: {
      background: 'var(--primary)',
      color: 'var(--on-primary)',
      border: '1px solid transparent'
    }
  };
  const v = variants[variant] || variants.cream;
  return /*#__PURE__*/React.createElement("button", _extends({
    "aria-label": ariaLabel,
    disabled: disabled,
    onClick: onClick,
    style: {
      display: 'inline-flex',
      alignItems: 'center',
      justifyContent: 'center',
      width: size,
      height: size,
      padding: 0,
      borderRadius: 'var(--radius-full)',
      cursor: disabled ? 'not-allowed' : 'pointer',
      opacity: disabled ? 0.5 : 1,
      transition: 'background var(--duration-fast) var(--ease-standard)',
      ...v,
      ...style
    }
  }, rest), children);
}
Object.assign(__ds_scope, { IconButton });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/buttons/IconButton.jsx", error: String((e && e.message) || e) }); }

// components/feedback/Badge.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/**
 * Badge — small pill label. Cream category pill or coral uppercase highlight.
 */
function Badge({
  children,
  variant = 'pill',
  style = {},
  ...rest
}) {
  const variants = {
    pill: {
      background: 'var(--surface-card)',
      color: 'var(--ink)',
      fontSize: 13,
      fontWeight: 500,
      letterSpacing: 0,
      textTransform: 'none'
    },
    coral: {
      background: 'var(--primary)',
      color: 'var(--on-primary)',
      fontSize: 12,
      fontWeight: 500,
      letterSpacing: '1.5px',
      textTransform: 'uppercase'
    },
    outline: {
      background: 'transparent',
      color: 'var(--muted)',
      border: '1px solid var(--hairline)',
      fontSize: 13,
      fontWeight: 500,
      letterSpacing: 0,
      textTransform: 'none'
    },
    teal: {
      background: 'rgba(93,184,166,0.16)',
      color: '#2f6e62',
      fontSize: 12,
      fontWeight: 500,
      letterSpacing: '1.5px',
      textTransform: 'uppercase'
    }
  };
  const v = variants[variant] || variants.pill;
  return /*#__PURE__*/React.createElement("span", _extends({
    style: {
      display: 'inline-flex',
      alignItems: 'center',
      gap: 6,
      padding: '4px 12px',
      borderRadius: 'var(--radius-pill)',
      fontFamily: 'var(--font-body)',
      lineHeight: 1.4,
      whiteSpace: 'nowrap',
      ...v,
      ...style
    }
  }, rest), children);
}
Object.assign(__ds_scope, { Badge });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/feedback/Badge.jsx", error: String((e && e.message) || e) }); }

// components/forms/Input.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/**
 * Input — text field with optional label, hint, and error state.
 * Cream fill, hairline border, coral focus ring.
 */
function Input({
  label,
  hint,
  error,
  id,
  value,
  onChange,
  placeholder,
  type = 'text',
  disabled = false,
  style = {},
  ...rest
}) {
  const [focused, setFocused] = React.useState(false);
  const inputId = id || React.useId();
  const borderColor = error ? 'var(--error)' : focused ? 'var(--primary)' : 'var(--hairline)';
  return /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      flexDirection: 'column',
      gap: 6,
      ...style
    }
  }, label && /*#__PURE__*/React.createElement("label", {
    htmlFor: inputId,
    style: {
      fontFamily: 'var(--font-body)',
      fontSize: 14,
      fontWeight: 500,
      color: 'var(--ink)'
    }
  }, label), /*#__PURE__*/React.createElement("input", _extends({
    id: inputId,
    type: type,
    value: value,
    onChange: onChange,
    placeholder: placeholder,
    disabled: disabled,
    onFocus: () => setFocused(true),
    onBlur: () => setFocused(false),
    style: {
      height: 40,
      padding: '10px 14px',
      fontFamily: 'var(--font-body)',
      fontSize: 16,
      color: 'var(--ink)',
      background: disabled ? 'var(--surface-soft)' : 'var(--canvas)',
      border: `1px solid ${borderColor}`,
      borderRadius: 'var(--radius-md)',
      outline: 'none',
      boxShadow: focused && !error ? '0 0 0 3px var(--focus-ring)' : 'none',
      transition: 'border-color var(--duration-fast), box-shadow var(--duration-fast)',
      width: '100%',
      boxSizing: 'border-box'
    }
  }, rest)), (hint || error) && /*#__PURE__*/React.createElement("span", {
    style: {
      fontFamily: 'var(--font-body)',
      fontSize: 13,
      color: error ? 'var(--error)' : 'var(--muted)'
    }
  }, error || hint));
}
Object.assign(__ds_scope, { Input });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/forms/Input.jsx", error: String((e && e.message) || e) }); }

// components/navigation/CategoryTabs.jsx
try { (() => {
/**
 * CategoryTabs — sub-nav filter row. Active tab fills with cream-card;
 * inactive tabs are muted text on transparent.
 */
function CategoryTabs({
  tabs = [],
  value,
  defaultValue,
  onChange,
  style = {}
}) {
  const [internal, setInternal] = React.useState(defaultValue ?? (tabs[0] && (tabs[0].value ?? tabs[0])));
  const active = value !== undefined ? value : internal;
  const select = val => {
    if (value === undefined) setInternal(val);
    onChange && onChange(val);
  };
  return /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'inline-flex',
      gap: 4,
      flexWrap: 'wrap',
      ...style
    },
    role: "tablist"
  }, tabs.map(t => {
    const val = t.value ?? t;
    const label = t.label ?? t;
    const isActive = val === active;
    return /*#__PURE__*/React.createElement("button", {
      key: val,
      role: "tab",
      "aria-selected": isActive,
      onClick: () => select(val),
      style: {
        padding: '8px 14px',
        borderRadius: 'var(--radius-md)',
        border: 'none',
        cursor: 'pointer',
        fontFamily: 'var(--font-body)',
        fontSize: 14,
        fontWeight: 500,
        lineHeight: 1.4,
        background: isActive ? 'var(--surface-card)' : 'transparent',
        color: isActive ? 'var(--ink)' : 'var(--muted)',
        transition: 'background var(--duration-fast), color var(--duration-fast)'
      }
    }, label);
  }));
}
Object.assign(__ds_scope, { CategoryTabs });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/navigation/CategoryTabs.jsx", error: String((e && e.message) || e) }); }

// components/surfaces/Card.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/**
 * Card — surface container. Drives the cream → dark → coral pacing system.
 * `feature` cream, `bordered` canvas+hairline, `dark` navy product chrome,
 * `coral` full-bleed callout.
 */
function Card({
  children,
  variant = 'feature',
  padding,
  style = {},
  ...rest
}) {
  const variants = {
    feature: {
      background: 'var(--surface-card)',
      color: 'var(--ink)',
      border: '1px solid transparent',
      pad: 32
    },
    bordered: {
      background: 'var(--canvas)',
      color: 'var(--ink)',
      border: '1px solid var(--hairline)',
      pad: 32
    },
    soft: {
      background: 'var(--surface-soft)',
      color: 'var(--ink)',
      border: '1px solid transparent',
      pad: 32
    },
    dark: {
      background: 'var(--surface-dark)',
      color: 'var(--on-dark)',
      border: '1px solid transparent',
      pad: 32
    },
    coral: {
      background: 'var(--primary)',
      color: 'var(--on-primary)',
      border: '1px solid transparent',
      pad: 48
    }
  };
  const v = variants[variant] || variants.feature;
  return /*#__PURE__*/React.createElement("div", _extends({
    style: {
      background: v.background,
      color: v.color,
      border: v.border,
      borderRadius: 'var(--radius-lg)',
      padding: padding != null ? padding : v.pad,
      ...style
    }
  }, rest), children);
}
Object.assign(__ds_scope, { Card });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/surfaces/Card.jsx", error: String((e && e.message) || e) }); }

// ui_kits/marketing/CTASection.jsx
try { (() => {
(function () {
  const {
    Button
  } = window.ClaudeDesignSystem_281e21;
  function CTASection({
    onTry
  }) {
    return /*#__PURE__*/React.createElement("section", {
      style: {
        padding: '96px 32px',
        background: 'var(--canvas)'
      }
    }, /*#__PURE__*/React.createElement("div", {
      style: {
        maxWidth: 'var(--container-max)',
        margin: '0 auto'
      }
    }, /*#__PURE__*/React.createElement("div", {
      style: {
        background: 'var(--coral)',
        borderRadius: 'var(--radius-lg)',
        padding: 64,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        flexWrap: 'wrap',
        gap: 32
      }
    }, /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("h2", {
      className: "t-display-md",
      style: {
        color: 'var(--on-primary)',
        margin: 0,
        fontFamily: 'var(--font-display)'
      }
    }, "Start building with Claude today"), /*#__PURE__*/React.createElement("p", {
      style: {
        color: 'rgba(255,255,255,0.85)',
        fontFamily: 'var(--font-body)',
        fontSize: 17,
        margin: '14px 0 0',
        maxWidth: 480
      }
    }, "Get started for free, or talk to our team about Claude for your enterprise.")), /*#__PURE__*/React.createElement("div", {
      style: {
        display: 'flex',
        gap: 12
      }
    }, /*#__PURE__*/React.createElement(Button, {
      variant: "on-coral",
      size: "lg",
      onClick: onTry
    }, "Try Claude"), /*#__PURE__*/React.createElement("button", {
      style: {
        background: 'transparent',
        border: '1px solid rgba(255,255,255,0.5)',
        color: 'var(--on-primary)',
        borderRadius: 'var(--radius-md)',
        padding: '0 26px',
        height: 48,
        fontFamily: 'var(--font-body)',
        fontSize: 15,
        fontWeight: 500,
        cursor: 'pointer'
      }
    }, "Contact sales")))));
  }
  Object.assign(window, {
    CTASection
  });
})();
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/marketing/CTASection.jsx", error: String((e && e.message) || e) }); }

// ui_kits/marketing/Features.jsx
try { (() => {
(function () {
  const {
    Card,
    CategoryTabs,
    Badge
  } = window.ClaudeDesignSystem_281e21;
  function Icon({
    d
  }) {
    return /*#__PURE__*/React.createElement("svg", {
      width: "22",
      height: "22",
      viewBox: "0 0 24 24",
      fill: "none",
      stroke: "var(--coral)",
      strokeWidth: "1.6",
      strokeLinecap: "round",
      strokeLinejoin: "round"
    }, d);
  }
  const icons = {
    brain: /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("path", {
      d: "M12 5a3 3 0 0 0-6 0v.5A3 3 0 0 0 5 11a3 3 0 0 0 1 5.7V17a3 3 0 0 0 6 0V5Z"
    }), /*#__PURE__*/React.createElement("path", {
      d: "M12 5a3 3 0 0 1 6 0v.5A3 3 0 0 1 19 11a3 3 0 0 1-1 5.7V17a3 3 0 0 1-6 0"
    })),
    code: /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("polyline", {
      points: "16 18 22 12 16 6"
    }), /*#__PURE__*/React.createElement("polyline", {
      points: "8 6 2 12 8 18"
    })),
    shield: /*#__PURE__*/React.createElement("path", {
      d: "M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10Z"
    }),
    zap: /*#__PURE__*/React.createElement("polygon", {
      points: "13 2 3 14 12 14 11 22 21 10 12 10 13 2"
    }),
    doc: /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("path", {
      d: "M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8Z"
    }), /*#__PURE__*/React.createElement("polyline", {
      points: "14 2 14 8 20 8"
    })),
    search: /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("circle", {
      cx: "11",
      cy: "11",
      r: "7"
    }), /*#__PURE__*/React.createElement("line", {
      x1: "21",
      y1: "21",
      x2: "16.65",
      y2: "16.65"
    }))
  };
  const FEATURES = [{
    i: 'brain',
    t: 'Extended thinking',
    d: 'Claude reasons step by step on complex problems, showing its work before it answers.'
  }, {
    i: 'code',
    t: 'Claude Code',
    d: 'An agentic coding partner that lives in your terminal and ships real changes across your repo.'
  }, {
    i: 'doc',
    t: 'Long context',
    d: 'Drop in entire codebases, contracts, or research libraries — Claude keeps it all in view.'
  }, {
    i: 'search',
    t: 'Web search & tools',
    d: 'Connect Claude to live data, internal systems, and the tools your team already uses.'
  }, {
    i: 'shield',
    t: 'Built for trust',
    d: 'Constitutional AI and enterprise controls keep your data private and your outputs safe.'
  }, {
    i: 'zap',
    t: 'Three model sizes',
    d: 'Opus for depth, Sonnet for balance, Haiku for speed. Switch as the task demands.'
  }];
  function Features() {
    const [cat, setCat] = React.useState('Capabilities');
    return /*#__PURE__*/React.createElement("section", {
      style: {
        padding: '96px 32px',
        background: 'var(--canvas)'
      }
    }, /*#__PURE__*/React.createElement("div", {
      style: {
        maxWidth: 'var(--container-max)',
        margin: '0 auto'
      }
    }, /*#__PURE__*/React.createElement("div", {
      style: {
        display: 'flex',
        alignItems: 'flex-end',
        justifyContent: 'space-between',
        flexWrap: 'wrap',
        gap: 24,
        marginBottom: 40
      }
    }, /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement(Badge, {
      variant: "pill"
    }, "Product"), /*#__PURE__*/React.createElement("h2", {
      className: "t-display-lg",
      style: {
        margin: '16px 0 0',
        maxWidth: 560
      }
    }, "Everything you need to do your most important work")), /*#__PURE__*/React.createElement(CategoryTabs, {
      tabs: ['Capabilities', 'For developers', 'For teams'],
      value: cat,
      onChange: setCat
    })), /*#__PURE__*/React.createElement("div", {
      style: {
        display: 'grid',
        gridTemplateColumns: 'repeat(3, 1fr)',
        gap: 20
      }
    }, FEATURES.map(f => /*#__PURE__*/React.createElement(Card, {
      key: f.t,
      variant: "feature"
    }, /*#__PURE__*/React.createElement(Icon, {
      d: icons[f.i]
    }), /*#__PURE__*/React.createElement("h3", {
      className: "t-title-md",
      style: {
        margin: '20px 0 8px'
      }
    }, f.t), /*#__PURE__*/React.createElement("p", {
      className: "t-body-md"
    }, f.d))))));
  }
  Object.assign(window, {
    Features
  });
})();
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/marketing/Features.jsx", error: String((e && e.message) || e) }); }

// ui_kits/marketing/Footer.jsx
try { (() => {
(function () {
  const Mark = window.Mark;
  const COLUMNS = [{
    h: 'Product',
    links: ['Claude', 'Claude Code', 'Max plan', 'Team plan', 'Enterprise', 'Pricing']
  }, {
    h: 'Solutions',
    links: ['Agents', 'Coding', 'Customer support', 'Education', 'Financial services']
  }, {
    h: 'Resources',
    links: ['Docs', 'API reference', 'Research', 'Customer stories', 'Status']
  }, {
    h: 'Company',
    links: ['About', 'Careers', 'Newsroom', 'Privacy', 'Responsible scaling']
  }];
  function Footer() {
    return /*#__PURE__*/React.createElement("footer", {
      style: {
        background: 'var(--surface-dark)',
        padding: '64px 32px 40px',
        borderTop: '1px solid #2a2825'
      }
    }, /*#__PURE__*/React.createElement("div", {
      style: {
        maxWidth: 'var(--container-max)',
        margin: '0 auto'
      }
    }, /*#__PURE__*/React.createElement("div", {
      style: {
        display: 'grid',
        gridTemplateColumns: '1.4fr repeat(4, 1fr)',
        gap: 32
      }
    }, /*#__PURE__*/React.createElement("div", {
      style: {
        display: 'flex',
        alignItems: 'center',
        gap: 10
      }
    }, /*#__PURE__*/React.createElement(Mark, {
      color: "#faf9f5",
      size: 24
    }), /*#__PURE__*/React.createElement("span", {
      style: {
        fontFamily: 'var(--font-display)',
        fontSize: 22,
        color: 'var(--on-dark)',
        letterSpacing: '-0.5px'
      }
    }, "Anthropic")), COLUMNS.map(c => /*#__PURE__*/React.createElement("div", {
      key: c.h
    }, /*#__PURE__*/React.createElement("div", {
      style: {
        fontFamily: 'var(--font-body)',
        fontSize: 13,
        fontWeight: 600,
        color: 'var(--on-dark)',
        marginBottom: 16
      }
    }, c.h), /*#__PURE__*/React.createElement("ul", {
      style: {
        listStyle: 'none',
        margin: 0,
        padding: 0,
        display: 'flex',
        flexDirection: 'column',
        gap: 11
      }
    }, c.links.map(l => /*#__PURE__*/React.createElement("li", {
      key: l
    }, /*#__PURE__*/React.createElement("a", {
      style: {
        fontFamily: 'var(--font-body)',
        fontSize: 14,
        color: 'var(--on-dark-soft)',
        textDecoration: 'none',
        cursor: 'pointer'
      }
    }, l))))))), /*#__PURE__*/React.createElement("div", {
      style: {
        marginTop: 56,
        paddingTop: 24,
        borderTop: '1px solid #2a2825',
        display: 'flex',
        justifyContent: 'space-between',
        flexWrap: 'wrap',
        gap: 16
      }
    }, /*#__PURE__*/React.createElement("span", {
      style: {
        fontFamily: 'var(--font-body)',
        fontSize: 13,
        color: 'var(--muted-soft)'
      }
    }, "\xA9 2026 Anthropic PBC"), /*#__PURE__*/React.createElement("div", {
      style: {
        display: 'flex',
        gap: 24
      }
    }, ['Terms', 'Privacy', 'Cookies', 'Usage policy'].map(l => /*#__PURE__*/React.createElement("a", {
      key: l,
      style: {
        fontFamily: 'var(--font-body)',
        fontSize: 13,
        color: 'var(--muted-soft)',
        textDecoration: 'none',
        cursor: 'pointer'
      }
    }, l))))));
  }
  Object.assign(window, {
    Footer
  });
})();
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/marketing/Footer.jsx", error: String((e && e.message) || e) }); }

// ui_kits/marketing/Hero.jsx
try { (() => {
(function () {
  const {
    Button,
    Badge
  } = window.ClaudeDesignSystem_281e21;
  function CodeWindow() {
    const tabs = ['agent.py', 'README.md'];
    const [tab, setTab] = React.useState('agent.py');
    return /*#__PURE__*/React.createElement("div", {
      style: {
        background: 'var(--surface-dark)',
        borderRadius: 'var(--radius-xl)',
        overflow: 'hidden',
        boxShadow: 'var(--shadow-card)'
      }
    }, /*#__PURE__*/React.createElement("div", {
      style: {
        display: 'flex',
        alignItems: 'center',
        gap: 8,
        padding: '14px 18px',
        borderBottom: '1px solid #2a2825'
      }
    }, /*#__PURE__*/React.createElement("span", {
      style: {
        width: 11,
        height: 11,
        borderRadius: '50%',
        background: '#3a3733'
      }
    }), /*#__PURE__*/React.createElement("span", {
      style: {
        width: 11,
        height: 11,
        borderRadius: '50%',
        background: '#3a3733'
      }
    }), /*#__PURE__*/React.createElement("span", {
      style: {
        width: 11,
        height: 11,
        borderRadius: '50%',
        background: '#3a3733'
      }
    }), /*#__PURE__*/React.createElement("div", {
      style: {
        display: 'flex',
        gap: 4,
        marginLeft: 14
      }
    }, tabs.map(t => /*#__PURE__*/React.createElement("button", {
      key: t,
      onClick: () => setTab(t),
      style: {
        background: tab === t ? 'var(--surface-dark-elevated)' : 'transparent',
        color: tab === t ? 'var(--on-dark)' : 'var(--on-dark-soft)',
        border: 'none',
        borderRadius: 'var(--radius-sm)',
        padding: '5px 12px',
        fontFamily: 'var(--font-mono)',
        fontSize: 12,
        cursor: 'pointer'
      }
    }, t)))), /*#__PURE__*/React.createElement("pre", {
      style: {
        margin: 0,
        padding: '20px 22px',
        fontFamily: 'var(--font-mono)',
        fontSize: 13.5,
        lineHeight: 1.7,
        color: 'var(--on-dark)',
        overflowX: 'auto'
      }
    }, tab === 'agent.py' ? /*#__PURE__*/React.createElement("code", null, /*#__PURE__*/React.createElement("span", {
      style: {
        color: '#8e8b82'
      }
    }, `# Build a research agent with Claude\n`), /*#__PURE__*/React.createElement("span", {
      style: {
        color: '#cc785c'
      }
    }, "from"), ` anthropic `, /*#__PURE__*/React.createElement("span", {
      style: {
        color: '#cc785c'
      }
    }, "import"), ` Anthropic\n\n`, `client = `, /*#__PURE__*/React.createElement("span", {
      style: {
        color: '#5db8a6'
      }
    }, "Anthropic"), `()\n\n`, `msg = client.messages.`, /*#__PURE__*/React.createElement("span", {
      style: {
        color: '#e8a55a'
      }
    }, "create"), `(\n`, `    model=`, /*#__PURE__*/React.createElement("span", {
      style: {
        color: '#9bbf8f'
      }
    }, "\"claude-opus-4\""), `,\n`, `    max_tokens=`, /*#__PURE__*/React.createElement("span", {
      style: {
        color: '#c9a26a'
      }
    }, "1024"), `,\n`, `    tools=[web_search, run_code],\n`, `    messages=[{`, /*#__PURE__*/React.createElement("span", {
      style: {
        color: '#9bbf8f'
      }
    }, "\"role\""), `: `, /*#__PURE__*/React.createElement("span", {
      style: {
        color: '#9bbf8f'
      }
    }, "\"user\""), `,\n`, `        `, /*#__PURE__*/React.createElement("span", {
      style: {
        color: '#9bbf8f'
      }
    }, "\"content\""), `: prompt}],\n`, `)\n`, /*#__PURE__*/React.createElement("span", {
      style: {
        color: '#8e8b82'
      }
    }, `# → Claude plans, searches, and writes the report`)) : /*#__PURE__*/React.createElement("code", null, /*#__PURE__*/React.createElement("span", {
      style: {
        color: '#8e8b82'
      }
    }, `# research-agent\n\n`), `An autonomous agent that plans\nmulti-step research with Claude.\n\n`, /*#__PURE__*/React.createElement("span", {
      style: {
        color: '#cc785c'
      }
    }, "## Quickstart"), `\n\n`, /*#__PURE__*/React.createElement("span", {
      style: {
        color: '#e8a55a'
      }
    }, "pip install"), ` anthropic\n`, /*#__PURE__*/React.createElement("span", {
      style: {
        color: '#e8a55a'
      }
    }, "python"), ` agent.py`)));
  }
  function Hero({
    onTry
  }) {
    return /*#__PURE__*/React.createElement("section", {
      style: {
        padding: '96px 32px',
        background: 'var(--canvas)'
      }
    }, /*#__PURE__*/React.createElement("div", {
      style: {
        maxWidth: 'var(--container-max)',
        margin: '0 auto',
        display: 'grid',
        gridTemplateColumns: '1fr 1.05fr',
        gap: 64,
        alignItems: 'center'
      }
    }, /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("div", {
      style: {
        marginBottom: 24
      }
    }, /*#__PURE__*/React.createElement(Badge, {
      variant: "coral"
    }, "Claude Opus 4")), /*#__PURE__*/React.createElement("h1", {
      className: "t-display-xl",
      style: {
        margin: 0
      }
    }, "AI that partners with your best thinking"), /*#__PURE__*/React.createElement("p", {
      className: "t-body-md",
      style: {
        marginTop: 24,
        fontSize: 19,
        lineHeight: 1.5,
        maxWidth: 440,
        color: 'var(--body-strong)'
      }
    }, "Claude is a thinking partner for your most important work \u2014 research, writing, analysis, and code."), /*#__PURE__*/React.createElement("div", {
      style: {
        display: 'flex',
        gap: 12,
        marginTop: 32
      }
    }, /*#__PURE__*/React.createElement(Button, {
      variant: "primary",
      size: "lg",
      onClick: onTry
    }, "Try Claude"), /*#__PURE__*/React.createElement(Button, {
      variant: "secondary",
      size: "lg"
    }, "Talk to sales"))), /*#__PURE__*/React.createElement(CodeWindow, null)));
  }
  Object.assign(window, {
    Hero
  });
})();
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/marketing/Hero.jsx", error: String((e && e.message) || e) }); }

// ui_kits/marketing/ProductShowcase.jsx
try { (() => {
(function () {
  const {
    Button,
    Badge
  } = window.ClaudeDesignSystem_281e21;
  const MODELS = [{
    name: 'Opus',
    tag: 'Most capable',
    blurb: 'Frontier intelligence for the hardest reasoning, agentic, and coding tasks.',
    bar: '100%'
  }, {
    name: 'Sonnet',
    tag: 'Balanced',
    blurb: 'The everyday workhorse — fast, smart, and cost-effective for most work.',
    bar: '78%'
  }, {
    name: 'Haiku',
    tag: 'Fastest',
    blurb: 'Near-instant responses for high-volume, latency-sensitive applications.',
    bar: '52%'
  }];
  function ProductShowcase() {
    return /*#__PURE__*/React.createElement("section", {
      style: {
        padding: '96px 32px',
        background: 'var(--surface-dark)'
      }
    }, /*#__PURE__*/React.createElement("div", {
      style: {
        maxWidth: 'var(--container-max)',
        margin: '0 auto'
      }
    }, /*#__PURE__*/React.createElement("div", {
      style: {
        textAlign: 'center',
        maxWidth: 620,
        margin: '0 auto 48px'
      }
    }, /*#__PURE__*/React.createElement("span", {
      style: {
        fontFamily: 'var(--font-body)',
        fontSize: 13,
        fontWeight: 500,
        letterSpacing: '1.5px',
        textTransform: 'uppercase',
        color: 'var(--accent-amber)'
      }
    }, "The Claude model family"), /*#__PURE__*/React.createElement("h2", {
      className: "t-display-lg",
      style: {
        color: 'var(--on-dark)',
        margin: '16px 0 0'
      }
    }, "Which problem are you up against?")), /*#__PURE__*/React.createElement("div", {
      style: {
        display: 'grid',
        gridTemplateColumns: 'repeat(3, 1fr)',
        gap: 20
      }
    }, MODELS.map(m => /*#__PURE__*/React.createElement("div", {
      key: m.name,
      style: {
        background: 'var(--surface-dark-elevated)',
        borderRadius: 'var(--radius-lg)',
        padding: 32
      }
    }, /*#__PURE__*/React.createElement("div", {
      style: {
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between'
      }
    }, /*#__PURE__*/React.createElement("span", {
      className: "t-display-sm",
      style: {
        color: 'var(--on-dark)',
        fontFamily: 'var(--font-display)'
      }
    }, "Claude ", m.name), /*#__PURE__*/React.createElement(Badge, {
      variant: "teal"
    }, m.tag)), /*#__PURE__*/React.createElement("div", {
      style: {
        height: 6,
        borderRadius: 999,
        background: '#34312d',
        marginTop: 24
      }
    }, /*#__PURE__*/React.createElement("div", {
      style: {
        width: m.bar,
        height: '100%',
        borderRadius: 999,
        background: 'var(--coral)'
      }
    })), /*#__PURE__*/React.createElement("p", {
      className: "t-body-md",
      style: {
        color: 'var(--on-dark-soft)',
        marginTop: 20
      }
    }, m.blurb), /*#__PURE__*/React.createElement("a", {
      style: {
        display: 'inline-block',
        marginTop: 16,
        color: 'var(--on-dark)',
        fontFamily: 'var(--font-body)',
        fontSize: 14,
        fontWeight: 500,
        textDecoration: 'none',
        borderBottom: '1px solid #4a4641',
        paddingBottom: 2,
        cursor: 'pointer'
      }
    }, "Learn more \u2192")))), /*#__PURE__*/React.createElement("div", {
      style: {
        display: 'flex',
        justifyContent: 'center',
        marginTop: 40
      }
    }, /*#__PURE__*/React.createElement(Button, {
      variant: "secondary-on-dark"
    }, "Compare all models"))));
  }
  Object.assign(window, {
    ProductShowcase
  });
})();
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/marketing/ProductShowcase.jsx", error: String((e && e.message) || e) }); }

// ui_kits/marketing/TopNav.jsx
try { (() => {
(function () {
  const {
    Button
  } = window.ClaudeDesignSystem_281e21;
  function Mark({
    color = '#141413',
    size = 26
  }) {
    return /*#__PURE__*/React.createElement("svg", {
      width: size,
      height: size,
      viewBox: "0 0 40 40",
      fill: color,
      "aria-hidden": "true",
      style: {
        display: 'block'
      }
    }, /*#__PURE__*/React.createElement("rect", {
      x: "18.4",
      y: "2",
      width: "3.2",
      height: "36",
      rx: "1"
    }), /*#__PURE__*/React.createElement("rect", {
      x: "18.4",
      y: "2",
      width: "3.2",
      height: "36",
      rx: "1",
      transform: "rotate(60 20 20)"
    }), /*#__PURE__*/React.createElement("rect", {
      x: "18.4",
      y: "2",
      width: "3.2",
      height: "36",
      rx: "1",
      transform: "rotate(120 20 20)"
    }));
  }
  function TopNav({
    onTry
  }) {
    const links = ['Claude', 'Solutions', 'Research', 'Commitments', 'Learn', 'Pricing'];
    const [open, setOpen] = React.useState(null);
    return /*#__PURE__*/React.createElement("header", {
      style: {
        position: 'sticky',
        top: 0,
        zIndex: 50,
        height: 64,
        background: 'var(--canvas)',
        borderBottom: '1px solid var(--hairline-soft)',
        display: 'flex',
        alignItems: 'center',
        padding: '0 32px',
        gap: 32
      }
    }, /*#__PURE__*/React.createElement("div", {
      style: {
        display: 'flex',
        alignItems: 'center',
        gap: 10
      }
    }, /*#__PURE__*/React.createElement(Mark, null), /*#__PURE__*/React.createElement("span", {
      style: {
        fontFamily: 'var(--font-display)',
        fontSize: 24,
        color: 'var(--ink)',
        letterSpacing: '-0.6px'
      }
    }, "Claude")), /*#__PURE__*/React.createElement("nav", {
      style: {
        display: 'flex',
        gap: 4,
        alignItems: 'center'
      }
    }, links.map(l => /*#__PURE__*/React.createElement("button", {
      key: l,
      onMouseEnter: () => setOpen(l),
      onMouseLeave: () => setOpen(null),
      style: {
        background: 'none',
        border: 'none',
        cursor: 'pointer',
        fontFamily: 'var(--font-body)',
        fontSize: 14,
        fontWeight: 500,
        color: open === l ? 'var(--ink)' : 'var(--body)',
        padding: '8px 12px',
        borderRadius: 'var(--radius-sm)'
      }
    }, l))), /*#__PURE__*/React.createElement("div", {
      style: {
        marginLeft: 'auto',
        display: 'flex',
        alignItems: 'center',
        gap: 8
      }
    }, /*#__PURE__*/React.createElement(Button, {
      variant: "text"
    }, "Sign in"), /*#__PURE__*/React.createElement(Button, {
      variant: "primary",
      onClick: onTry
    }, "Try Claude")));
  }
  Object.assign(window, {
    TopNav,
    Mark
  });
})();
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/marketing/TopNav.jsx", error: String((e && e.message) || e) }); }

__ds_ns.Button = __ds_scope.Button;

__ds_ns.IconButton = __ds_scope.IconButton;

__ds_ns.Badge = __ds_scope.Badge;

__ds_ns.Input = __ds_scope.Input;

__ds_ns.CategoryTabs = __ds_scope.CategoryTabs;

__ds_ns.Card = __ds_scope.Card;

})();
