// Every animated image (the finished games, and the originals that are GIFs) gets a button that
// pauses it on the current frame and plays it again (WCAG 2.2.2: moving content longer than five
// seconds can be paused). With "reduce motion" set in the operating system, they start paused.
document.addEventListener("DOMContentLoaded", () => {
  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches
  const images = document.querySelectorAll(
    '.sl-markdown-content img[alt^="The finished"], .sl-markdown-content img[src$=".gif"]',
  )

  for (const img of images) {
    const wrap = document.createElement("span")
    wrap.className = "anim-wrap"
    img.replaceWith(wrap)
    wrap.append(img)

    const button = document.createElement("button")
    button.type = "button"
    button.className = "anim-toggle"
    wrap.append(button)

    let still = null
    const show = (paused) => {
      button.textContent = paused ? "▶︎" : "❚❚"   // text-style symbols, not emoji
      button.setAttribute("aria-label", paused ? "Play the animation" : "Pause the animation")
    }
    const pause = () => {
      // A canvas over the image holds the frame that was showing.
      still = document.createElement("canvas")
      still.width = img.naturalWidth
      still.height = img.naturalHeight
      still.getContext("2d").drawImage(img, 0, 0)
      still.setAttribute("aria-hidden", "true")
      wrap.insertBefore(still, button)
      show(true)
    }
    const play = () => {
      still?.remove()
      still = null
      show(false)
    }

    button.addEventListener("click", () => (still ? play() : pause()))
    show(false)
    if (reduceMotion) {
      if (img.complete && img.naturalWidth) pause()
      else img.addEventListener("load", pause, { once: true })
    }
  }
})
