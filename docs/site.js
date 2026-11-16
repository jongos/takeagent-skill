const platforms = {
claude: ["CUSTOM SKILL + CONNECTOR", "Add It to Claude.", "Upload the ZIP in Customize → Skills and enable it. For connected tools, add TakeAgent as a remote MCP connector and sign in with your own account."],
chatgpt: ["INSTRUCTIONS + MCP", "Set It Up in ChatGPT.", "Use the skill facility where available, or add the skill files to your project instructions. For connected tools, add the TakeAgent MCP server where your account or workspace permits custom connections."],
gemini: ["CLI SKILL · APP GUIDANCE", "Choose Your Gemini Surface.", "Gemini CLI supports Agent Skills and compatible MCP connections. In the Gemini app, use the available custom instruction feature for guidance; a connected TakeAgent install is not yet verified."],
grok: ["GUIDANCE · DEVELOPER MCP", "Bring the Instructions to Grok.", "Use the skill files as instructions where supported. Developers can integrate remote MCP with per-user TakeAgent OAuth. Native skill installation and connected use in the Grok consumer app remain unverified."]
};
const tabs = [...document.querySelectorAll('[role="tab"]')];
function select(tab) {
  tabs.forEach(t => {t.setAttribute("aria-selected", String(t === tab)); t.tabIndex = t === tab ? 0 : -1;});
  const [mode, title, copy] = platforms[tab.dataset.platform];
  document.getElementById("mode").textContent = mode;
  document.getElementById("platform-title").textContent = title;
  document.getElementById("platform-copy").textContent = copy;
  document.getElementById("panel").setAttribute("aria-labelledby", tab.id);
}
tabs.forEach((tab, index) => {
  tab.addEventListener("click", () => select(tab));
  tab.addEventListener("keydown", event => {
    let next;
    if(event.key === "ArrowRight") next = (index + 1) % tabs.length;
    if(event.key === "ArrowLeft") next = (index + tabs.length - 1) % tabs.length;
    if(event.key === "Home") next = 0;
    if(event.key === "End") next = tabs.length - 1;
    if(next !== undefined) {event.preventDefault(); select(tabs[next]); tabs[next].focus();}
  });
});
document.getElementById("copy").addEventListener("click", async () => {
  try {
    await navigator.clipboard.writeText("https://takeagent.ai/api/mcp");
    document.getElementById("copy-status").textContent = "Server URL copied.";
  } catch {
    document.getElementById("copy-status").textContent = "Select and copy the server URL above.";
  }
});
