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
  
    fetch("/api/get_ip_info")
      .then((response) => response.json())
      .then((data) => {
        document.getElementById("ip").textContent = data.ip;
        document.getElementById("city").textContent = data.city;
        document.getElementById("region").textContent = data.region;
        document.getElementById("country").textContent = data.country_name;
        document.getElementById("isp").textContent = data.org;
        document.getElementById("asn").textContent = data.asn;
        document.getElementById("latlng").textContent = `${data.latitude}, ${data.longitude}`;
  
        document.getElementById("loading").style.display = "none";
        document.getElementById("ip-info").style.display = "block";
      })
      .catch((error) => {
        console.error("Error fetching IP info:", error);
        alert("Failed to fetch IP information.");
        document.getElementById("loading").style.display = "none";
      });
  });
  