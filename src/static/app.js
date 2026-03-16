document.addEventListener("DOMContentLoaded", () => {
  const activitiesList = document.getElementById("activities-list");
  const activitySelect = document.getElementById("activity");
  const signupForm = document.getElementById("signup-form");
  const messageDiv = document.getElementById("message");
  const defaultActivityOption = '<option value="">-- Select an activity --</option>';

  function showMessage(message, type) {
    messageDiv.textContent = message;
    messageDiv.className = `message ${type}`;
    messageDiv.classList.remove("hidden");

    setTimeout(() => {
      messageDiv.classList.add("hidden");
    }, 5000);
  }

  function escapeHtml(value) {
    return String(value)
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;")
      .replaceAll('"', "&quot;")
      .replaceAll("'", "&#39;");
  }

  // Function to fetch activities from API
  async function fetchActivities() {
    try {
      const response = await fetch(`/activities?_=${Date.now()}`, {
        cache: "no-store",
      });
      const activities = await response.json();

      // Clear loading message
      activitiesList.innerHTML = "";
      activitySelect.innerHTML = defaultActivityOption;

      // Populate activities list
      Object.entries(activities).forEach(([name, details]) => {
        const activityCard = document.createElement("div");
        activityCard.className = "activity-card";

        const participants = Array.isArray(details.participants) ? details.participants : [];
        const maxParticipants = Number(details.max_participants) || 0;
        const spotsLeft = Math.max(maxParticipants - participants.length, 0);
        const participantCount = participants.length;
        const availabilityClass =
          spotsLeft === 0
            ? "availability-badge full"
            : spotsLeft <= 3
              ? "availability-badge limited"
              : "availability-badge";
        const availabilityLabel = spotsLeft === 0 ? "Full" : `${spotsLeft} spots left`;
        const participantsMarkup = participantCount
          ? `
            <ul class="participants-list">
              ${participants
                .map(
                  (participant) => `
                    <li class="participant-item">
                      <span class="participant-email">${escapeHtml(participant)}</span>
                      <button
                        type="button"
                        class="participant-delete-btn"
                        data-activity="${escapeHtml(name)}"
                        data-email="${escapeHtml(participant)}"
                        aria-label="Unregister ${escapeHtml(participant)}"
                        title="Unregister participant"
                      >
                        <svg viewBox="0 0 24 24" aria-hidden="true" focusable="false">
                          <path d="M4 7h16" />
                          <path d="M10 11v6" />
                          <path d="M14 11v6" />
                          <path d="M6 7l1 13h10l1-13" />
                          <path d="M9 7V4h6v3" />
                        </svg>
                      </button>
                    </li>
                  `
                )
                .join("")}
            </ul>
          `
          : '<p class="participants-empty">No students signed up yet.</p>';

        activityCard.innerHTML = `
          <div class="activity-card-header">
            <h4>${escapeHtml(name)}</h4>
            <span class="${availabilityClass}">${availabilityLabel}</span>
          </div>
          <p class="activity-description">${escapeHtml(details.description)}</p>
          <p class="activity-schedule"><strong>Schedule:</strong> ${escapeHtml(details.schedule)}</p>
          <div class="participants-section">
            <div class="participants-heading">
              <h5>Participants</h5>
              <span class="participant-count">${participantCount} enrolled</span>
            </div>
            ${participantsMarkup}
          </div>
        `;

        activitiesList.appendChild(activityCard);

        // Add option to select dropdown
        const option = document.createElement("option");
        option.value = name;
        option.textContent = name;
        activitySelect.appendChild(option);
      });
    } catch (error) {
      activitiesList.innerHTML = "<p>Failed to load activities. Please try again later.</p>";
      console.error("Error fetching activities:", error);
    }
  }

  // Handle form submission
  signupForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const email = document.getElementById("email").value;
    const activity = document.getElementById("activity").value;

    try {
      const response = await fetch(
        `/activities/${encodeURIComponent(activity)}/signup?email=${encodeURIComponent(email)}`,
        {
          method: "POST",
        }
      );

      const result = await response.json();

      if (response.ok) {
        showMessage(result.message, "success");
        signupForm.reset();
        await fetchActivities();
      } else {
        showMessage(result.detail || "An error occurred", "error");
      }
    } catch (error) {
      showMessage("Failed to sign up. Please try again.", "error");
      console.error("Error signing up:", error);
    }
  });

  activitiesList.addEventListener("click", async (event) => {
    const removeButton = event.target.closest(".participant-delete-btn");
    if (!removeButton) {
      return;
    }

    const { activity: activityName, email } = removeButton.dataset;
    if (!activityName || !email) {
      return;
    }

    removeButton.disabled = true;

    try {
      const response = await fetch(
        `/activities/${encodeURIComponent(activityName)}/unregister?email=${encodeURIComponent(email)}`,
        {
          method: "POST",
        }
      );

      const result = await response.json();

      if (response.ok) {
        showMessage(result.message, "success");
        await fetchActivities();
      } else {
        showMessage(result.detail || "Unable to unregister participant.", "error");
      }
    } catch (error) {
      showMessage("Failed to unregister participant. Please try again.", "error");
      console.error("Error unregistering participant:", error);
    } finally {
      removeButton.disabled = false;
    }
  });

  // Initialize app
  fetchActivities();
});
