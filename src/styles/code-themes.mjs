// The colours of code samples, in the course's own palette: orange for keywords, teal for
// types (as in the figures), sand for functions and green for strings. Only the token
// colours are set here; the frames and backgrounds follow the site's theme.

/** @param {"dark" | "light"} type @param {Record<string, string>} c */
function theme(type, c) {
  const rule = (scope, foreground, fontStyle) => ({
    scope,
    settings: fontStyle ? { foreground, fontStyle } : { foreground },
  })
  return {
    name: `gar-${type}`,
    type,
    colors: {
      "editor.background": c.background,
      "editor.foreground": c.text,
    },
    tokenColors: [
      rule(["comment", "punctuation.definition.comment"], c.comment, "italic"),
      rule(["keyword", "storage", "storage.modifier", "storage.type", "keyword.control", "keyword.other"], c.keyword),
      rule(["keyword.operator", "punctuation", "meta.brace", "meta.delimiter"], c.punctuation),
      rule(["keyword.type", "entity.name.type", "entity.name.class", "entity.name.namespace", "support.type", "support.class", "entity.other.inherited-class"], c.type),
      rule(["entity.name.function", "support.function", "meta.function-call entity.name.function"], c.function),
      rule(["string", "string.quoted", "punctuation.definition.string"], c.string),
      rule(["constant.numeric", "constant.language", "constant.character", "constant.other"], c.constant),
      rule(["variable.other.object.property", "variable.other.property", "support.type.property-name", "entity.other.attribute-name"], c.property),
      rule(["entity.name.tag", "punctuation.definition.tag"], c.keyword),
      rule(["variable", "variable.other.readwrite", "entity.name.variable"], c.text),
    ],
  }
}

export const garDark = theme("dark", {
  background: "#2b2421",
  text: "#e9dfd8",
  comment: "#9c8d83",
  keyword: "#ee8a63",
  punctuation: "#bfb1a7",
  type: "#5fc7c2",
  function: "#ecd08f",
  string: "#a3d391",
  constant: "#f3b693",
  property: "#dbc8b9",
})

export const garLight = theme("light", {
  background: "#f8f6f5",
  text: "#2b2420",
  comment: "#7d7068",
  keyword: "#b0431a",
  punctuation: "#5c504a",
  type: "#0c7572",
  function: "#7a5600",
  string: "#356f24",
  constant: "#9a4a1f",
  property: "#4a3b33",
})
