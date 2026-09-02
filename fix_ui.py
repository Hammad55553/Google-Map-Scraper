with open("frontend/src/app/page.tsx", "r") as f:
    content = f.read()

# First, revert ALL "</div></section>" back to "</section>"
content = content.replace("</div></section>", "</section>")

# Now, we only needed that extra </div> at the end of the Table section.
# The table section ends around line 493. Let's find the closing table tags:
old_table_end = """              )}
            </tbody>
          </table>
        </section>"""
new_table_end = """              )}
            </tbody>
          </table>
          </div>
        </section>"""
content = content.replace(old_table_end, new_table_end)

with open("frontend/src/app/page.tsx", "w") as f:
    f.write(content)
