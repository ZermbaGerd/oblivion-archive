// <!-- TODO: move this back into Flask so it automatically draws from entries.txt -->
// <!-- TODO: make this much prettier. show the preview image -->


names = ["Example",
        "Second_Example",
        "Instagram_Account_-_Cristiano_Ronaldo",
        "Notre-Dame_de_Paris"]

for (const name of names) {
    document.getElementById("entryList").append(createEntryLink(name))
}

function createEntryLink(name) {
    let entryLink = document.createElement("a")
    entryLink.className = "entryLink"
    entryLink.id=name
    entryLink.innerText = name.replaceAll("_", " ") + "\n"
    entryLink.setAttribute("href", "/entry/"+name)

    return entryLink
}


//  rudimentary reset button
function createResetButton() {
    resetButton = document.createElement("button")
    resetButton.id = "resetButton"
    resetButton.innerText = "Reset Entries"

    resetButton.addEventListener("click", () => {
        console.log("tried to reset cookies");
        fetch("/reset_entries")
            .catch((error) => {
                alert("Resetting the entries failed")
            })
    })
    document.body.appendChild(resetButton)
}

createResetButton()