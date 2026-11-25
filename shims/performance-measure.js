{
  const measure = Performance.prototype.measure
  Performance.prototype.measure = function (...args) {
    try {
      return measure.apply(this, args)
    } catch {
      return undefined
    }
  }
}
