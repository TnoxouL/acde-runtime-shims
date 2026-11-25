{
  const KINDS = [
    [Element, 1, null],
    [Text, 3, '#text'],
    [Comment, 8, '#comment'],
    [Document, 9, '#document'],
    [DocumentFragment, 11, '#document-fragment'],
  ]
  const elementName = Object.getOwnPropertyDescriptor(Element.prototype, 'nodeName')?.get

  function patch(property, empty, fallback) {
    const descriptor = Object.getOwnPropertyDescriptor(Node.prototype, property)
    if (!descriptor?.get) return
    const original = descriptor.get
    Object.defineProperty(Node.prototype, property, {
      ...descriptor,
      get() {
        const own = original.call(this)
        if (own !== empty) return own
        for (const kind of KINDS) {
          if (this instanceof kind[0]) return fallback(this, kind)
        }
        return own
      },
    })
  }

  patch('nodeType', 0, (_node, kind) => kind[1])
  patch('nodeName', '', (node, kind) => (kind[0] === Element && elementName ? elementName.call(node) : kind[2]))
}
