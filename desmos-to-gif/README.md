A tool I made to export a Desmos graph to a GIF after becoming unsatisfied with laggy screen recorders and online tools. Can be used to share the animated screenshot of a Desmos graph on a social platform like Instagram.

To use:

- Go to `https://www.desmos.com/calculator/<graph_id>`
- Press F12 to open developer tool. Dock it to the right.
- Adjust the horizontal position of the sidebars to make the canvas appear square.
- Scroll and drag the graph to an appropriate size and position.
- Copy the content of `desmos-gif.js` to the console of the developer tool. Change `IMAGE_SIZE` and `FRAME_COUNT` appropriately and run the script.
- The script will animate the first slider in the list of expressions. If the bounds of the slider is unset or not numerical (ex. `2\pi`), it will log a warning in the console and use default bounds.
- After the script finished running, copy the HTML inside the console and save it as a local file.
- Run `desmos_to_gif.py`. Enter the path to the saved file, a filename with extension `.gif`, `.webp`, or `.png`, and the speed of the animation (can be found when click the animation mode button of the slider on Desmos).
- If you need, you can search for online tools to convert a WebP or APNG image to a MP4 video.
