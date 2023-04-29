const onSelectTheme = async (id,name) => {
  await fetch("/select-theme/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken,
    },
    body: JSON.stringify({
      id
    }),
  })
    .then((response) => Toastify({
            text: `${name} theme selected successfully`,
            duration: 3000
        }).showToast())
    .catch((error) => console.log(" Error ", error));
};
