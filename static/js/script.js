tailwind.config = {
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        mustard: "#FFDB58",
      },
    },
  },
};

const themeToggleBtn = document.getElementById("theme-toggle");
const body = document.body;

const darkModeEnabled = localStorage.getItem("darkMode") === "true";
if (darkModeEnabled) {
  body.classList.add("dark");
  themeToggleBtn.innerHTML = "<i class='bx bx-sun'></i>";
}

themeToggleBtn.addEventListener("click", function () {
  body.classList.toggle("dark");

  if (body.classList.contains("dark")) {
    themeToggleBtn.innerHTML = "<i class='bx bx-sun'></i>";
    localStorage.setItem("darkMode", "true");
  } else {
    themeToggleBtn.innerHTML = "<i class='bx bx-moon'></i>";
    localStorage.setItem("darkMode", "false");
  }
});

document.getElementById("fetch-ip-btn").addEventListener("click", function () {
  document.getElementById("loading").style.display = "block";
  document.getElementById("ip-info").style.display = "none";

  async function fetchIPInfo() {
    try {
      const response = await fetch("/get_ip_info");
      const data = await response.json();

      if (data.error) {
        document.getElementById("ip-info").innerText = `Error: ${data.error}`;
      } else {
        // IP Addresses
        document.getElementById("ipv4").textContent = data.ipv4 || "N/A";
        document.getElementById("ipv6").textContent = data.ipv6 || "N/A";

        // Location Data
        document.getElementById("city").textContent = data.city || "N/A";
        document.getElementById("region").textContent = data.region || "N/A";
        document.getElementById("country").textContent = data.country || "N/A";
        document.getElementById("isp").textContent = data.org || "N/A";
        document.getElementById("asn").textContent = data.asn || "N/A";
        document.getElementById("latlng").textContent =
          `${data.latitude}, ${data.longitude}` || "N/A";

        document.getElementById("loading").style.display = "none";
        document.getElementById("ip-info").style.display = "block";

        // Speed Test Data
        document.getElementById("download_speed").textContent =
          data.speed_test?.download_speed_mbps || "N/A";
        document.getElementById("upload_speed").textContent =
          data.speed_test?.upload_speed_mbps || "N/A";
        document.getElementById("ping").textContent =
          data.speed_test?.ping_ms || "N/A";

        document.getElementById("loading").style.display = "none";
        document.getElementById("speed-info").style.display = "block";
      }
    } catch (error) {
      console.error("Error fetching IP info:", error);
      alert("Failed to fetch IP information.");
      document.getElementById("loading").style.display = "none";
    }
  }

  fetchIPInfo();
});
