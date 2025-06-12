document.getElementById("uploadForm").onsubmit = async (e) => {
  e.preventDefault();
  const formData = new FormData(e.target);

  const res = await fetch("/sign", {
    method: "POST",
    body: formData,
  });

  const data = await res.json();

  // ✅ Đảm bảo có key 'signature' và 'public_key'
  document.getElementById("signature").value = data.signature || "Không có chữ ký!";
  document.getElementById("publicKey").value = data.public_key || "Không có khóa!";
  document.getElementById("result").style.display = "block";
};
