import { ref, onMounted, onUnmounted, computed } from "vue";
import { useRouter } from "vue-router";
import { getQuizzes, getQuestions, getChapters, getSubjects } from "../api";

const router = useRouter();
const userFullName = ref("");
const quizzes = ref([]);
const questions = ref([]);
const chapters = ref([]);
const subjects = ref([]);

// Quiz state
const selectedQuiz = ref(null);
const quizQuestions = ref([]);
const currentQuestionIndex = ref(0);
const selectedAnswers = ref({});
const timeRemaining = ref(0);
const quizDuration = ref(0);
const showResults = ref(false);
const correctAnswers = ref(0);
const completedQuizzes = ref([]);
let timer = null;

// Add new reactive variables for quiz summary
const showQuizSummary = ref(false);
const quizResults = ref([]);
const performanceTrend = ref(5.2); // Mock data - would come from API
const studyStreak = ref(7); // Mock data - would come from API

// Add new reactive variables for quiz filtering and organization
const activeFilter = ref("all");
const searchQuery = ref("");
const sortBy = ref("date");

// Add sidebar functionality
const isSidebarCollapsed = ref(false);

const toggleSidebar = () => {
  isSidebarCollapsed.value = !isSidebarCollapsed.value;
};

// Computed properties for filtered and sorted quizzes
const filteredQuizzes = computed(() => {
  let filtered = quizzes.value;

  // Filter by status
  if (activeFilter.value === "active") {
    filtered = filtered.filter((quiz) => quiz.status === "active");
  } else if (activeFilter.value === "upcoming") {
    filtered = filtered.filter((quiz) => quiz.status === "upcoming");
  } else if (activeFilter.value === "expired") {
    filtered = filtered.filter((quiz) => quiz.status === "expired");
  }

  // Filter by search query
  if (searchQuery.value.trim()) {
    const query = searchQuery.value.toLowerCase();
    filtered = filtered.filter(
      (quiz) =>
        quiz.title.toLowerCase().includes(query) ||
        getSubjectNameFromChapter(quiz.chapter_id)
          .toLowerCase()
          .includes(query) ||
        getChapterName(quiz.chapter_id).toLowerCase().includes(query)
    );
  }

  // Sort quizzes
  filtered = [...filtered].sort((a, b) => {
    switch (sortBy.value) {
      case "title":
        return a.title.localeCompare(b.title);
      case "duration":
        const durationA = a.duration_hours * 60 + a.duration_minutes;
        const durationB = b.duration_hours * 60 + b.duration_minutes;
        return durationA - durationB;
      case "subject":
        return getSubjectNameFromChapter(a.chapter_id).localeCompare(
          getSubjectNameFromChapter(b.chapter_id)
        );
      case "date":
      default:
        return new Date(a.start_datetime) - new Date(b.start_datetime);
    }
  });

  return filtered;
});

const activeQuizzes = computed(() => {
  return quizzes.value.filter((quiz) => quiz.status === "active");
});

const upcomingQuizzes = computed(() => {
  return quizzes.value.filter((quiz) => quiz.status === "upcoming");
});

const expiredQuizzes = computed(() => {
  return quizzes.value.filter((quiz) => quiz.status === "expired");
});

const currentQuestion = computed(() => {
  return quizQuestions.value[currentQuestionIndex.value] || null;
});

const logout = () => {
  localStorage.removeItem("token");
  localStorage.removeItem("role");
  router.push("/login");
};

const isLoading = ref(true);

const fetchData = async () => {
  isLoading.value = true;
  try {
    console.log("📊 Fetching all data...");

    // Fetch quizzes first - this is the most important
    try {
      quizzes.value = await getQuizzes();
      console.log("📊 Quizzes loaded:", quizzes.value.length);
      console.log("📊 Quiz data:", quizzes.value);

      // Log each quiz's status
      quizzes.value.forEach((quiz, index) => {
        console.log(`📊 Quiz ${index + 1}:`, {
          id: quiz.id,
          title: quiz.title,
          status: quiz.status,
          start_datetime: quiz.start_datetime,
          end_datetime: quiz.end_datetime,
        });
      });
    } catch (error) {
      console.error("📊 Error loading quizzes:", error);
      quizzes.value = [];
    }

    // Fetch other data (these are less critical)
    try {
      questions.value = await getQuestions();
    } catch (error) {
      console.error("Error loading questions:", error);
      questions.value = [];
    }

    try {
      chapters.value = await getChapters();
    } catch (error) {
      console.error("Error loading chapters:", error);
      chapters.value = [];
    }

    try {
      subjects.value = await getSubjects();
    } catch (error) {
      console.error("Error loading subjects:", error);
      subjects.value = [];
    }

    // Fetch quiz history
    try {
      await fetchQuizHistory();
    } catch (error) {
      console.error("Error loading quiz history:", error);
    }

    console.log("All data loaded successfully");
  } finally {
    isLoading.value = false;
  }
};

const fetchQuizHistory = async () => {
  try {
    console.log("Fetching quiz history...");
    const response = await fetch("http://127.0.0.1:5006/api/quiz-history", {
      headers: {
        Authorization: `Bearer ${localStorage.getItem("token")}`,
        "Content-Type": "application/json",
      },
    });

    if (response.ok) {
      const history = await response.json();
      completedQuizzes.value = history.map((score) => score.quiz_id);
      console.log(
        "Quiz history loaded. Completed quizzes:",
        completedQuizzes.value
      );
    } else {
      console.error("Failed to fetch quiz history:", response.status);
    }
  } catch (error) {
    console.error("Error fetching quiz history:", error);
  }
};

const getStatusBadge = (status) => {
  const statusMap = {
    active: { class: "badge bg-success", text: "Active" },
    upcoming: { class: "badge bg-warning", text: "Upcoming" },
    expired: { class: "badge bg-danger", text: "Expired" },
  };
  return statusMap[status] || { class: "badge bg-secondary", text: "Unknown" };
};

const getSubjectNameFromChapter = (chapterId) => {
  const chapter = chapters.value.find((c) => c.id === chapterId);
  if (!chapter) return "Unknown";
  const subject = subjects.value.find((s) => s.id === chapter.subject_id);
  return subject ? subject.name : "Unknown";
};

const getChapterName = (chapterId) => {
  const chapter = chapters.value.find((c) => c.id === chapterId);
  return chapter ? chapter.name : "Unknown";
};

const getDifficultyBadge = (difficulty) => {
  const difficultyMap = {
    easy: { class: "badge bg-success", text: "Easy" },
    medium: { class: "badge bg-warning", text: "Medium" },
    hard: { class: "badge bg-danger", text: "Hard" },
  };
  return (
    difficultyMap[difficulty] || {
      class: "badge bg-secondary",
      text: "Unknown",
    }
  );
};

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString("en-US", {
    year: "numeric",
    month: "short",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
};

const formatTime = (seconds) => {
  const hours = Math.floor(seconds / 3600);
  const minutes = Math.floor((seconds % 3600) / 60);
  const secs = seconds % 60;

  if (hours > 0) {
    return `${hours}:${minutes.toString().padStart(2, "0")}:${secs
      .toString()
      .padStart(2, "0")}`;
  }
  return `${minutes}:${secs.toString().padStart(2, "0")}`;
};

const debugSelectQuiz = async (quiz) => {
  console.log("🔧 DEBUG: debugSelectQuiz called with:", quiz);
  console.log("🔧 DEBUG: Quiz status:", quiz.status);
  console.log(
    "🔧 DEBUG: Quiz completed:",
    completedQuizzes.value.includes(quiz.id)
  );

  try {
    selectedQuiz.value = quiz;
    console.log("🔧 DEBUG: selectedQuiz set to:", selectedQuiz.value);

    // Try to fetch questions
    const response = await fetch(
      `http://127.0.0.1:5006/api/test-quiz/${quiz.id}`,
      {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`,
          "Content-Type": "application/json",
        },
      }
    );

    console.log("🔧 DEBUG: Response status:", response.status);

    if (response.ok) {
      const data = await response.json();
      console.log("🔧 DEBUG: Quiz data received:", data);
      quizQuestions.value = data.questions || [];
      console.log("🔧 DEBUG: Questions set:", quizQuestions.value);
    } else {
      console.log("🔧 DEBUG: Response not ok, trying fallback");
      quizQuestions.value = questions.value.filter(
        (q) => q.quiz_id === quiz.id
      );
      console.log("🔧 DEBUG: Fallback questions:", quizQuestions.value);
    }

    selectedAnswers.value = {};
    currentQuestionIndex.value = 0;
    showResults.value = false;

    console.log("🔧 DEBUG: Quiz setup completed");
  } catch (error) {
    console.error("🔧 DEBUG: Error in debugSelectQuiz:", error);
  }
};

const selectQuiz = async (quiz) => {
  console.log("🚀 selectQuiz function called!"); // Simple debug log
  console.log("=== selectQuiz function called ==="); // Debug log
  console.log("selectQuiz called with:", quiz); // Debug log
  console.log("Quiz status from backend:", quiz.status); // Debug log
  console.log("Is completed:", completedQuizzes.value.includes(quiz.id)); // Debug log
  console.log("Token exists:", !!localStorage.getItem("token")); // Debug log

  // Check if quiz is already completed
  if (completedQuizzes.value.includes(quiz.id)) {
    console.log("Quiz already completed, returning"); // Debug log
    alert("You have already completed this quiz. You cannot take it again.");
    return;
  }

  // Use the status from the backend API
  if (quiz.status === "expired") {
    console.log("Quiz expired, returning"); // Debug log
    alert("This quiz has expired and is no longer available.");
    return;
  }

  if (quiz.status === "upcoming") {
    console.log("Quiz upcoming, returning"); // Debug log
    alert("This quiz is not yet available. Please wait until the start time.");
    return;
  }

  if (quiz.status !== "active") {
    console.log("Quiz not active, returning. Status:", quiz.status); // Debug log
    alert("This quiz is not currently active. Please select an active quiz.");
    return;
  }

  console.log("All checks passed, proceeding with quiz selection"); // Debug log

  try {
    console.log("Setting selectedQuiz to:", quiz); // Debug log
    selectedQuiz.value = quiz;

    // Fetch questions for this specific quiz
    console.log("Fetching questions for quiz ID:", quiz.id); // Debug log
    const quizQuestionsResponse = await fetch(
      `http://127.0.0.1:5006/api/test-quiz/${quiz.id}`,
      {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`,
          "Content-Type": "application/json",
        },
      }
    );

    console.log(
      "Quiz questions response status:",
      quizQuestionsResponse.status
    ); // Debug log

    if (quizQuestionsResponse.ok) {
      const quizData = await quizQuestionsResponse.json();
      console.log("Quiz data received:", quizData); // Debug log
      quizQuestions.value = quizData.questions || [];
      console.log("Quiz questions set:", quizQuestions.value); // Debug log
    } else {
      console.log("Fallback to filtering from all questions"); // Debug log
      // Fallback to filtering from all questions
      quizQuestions.value = questions.value.filter(
        (q) => q.quiz_id === quiz.id
      );
      console.log("Filtered questions:", quizQuestions.value); // Debug log
    }

    selectedAnswers.value = {};
    currentQuestionIndex.value = 0;
    showResults.value = false;

    // Set timer
    quizDuration.value =
      quiz.duration_hours * 3600 + quiz.duration_minutes * 60;
    timeRemaining.value = quizDuration.value;

    console.log("Starting timer with duration:", quizDuration.value); // Debug log
    startTimer();
    console.log("=== selectQuiz function completed successfully ==="); // Debug log
  } catch (error) {
    console.error("Error fetching quiz questions:", error);
    console.error("Error details:", error.message); // Debug log
    alert("Error loading quiz questions. Please try again.");
  }
};

const startTimer = () => {
  timer = setInterval(() => {
    if (timeRemaining.value > 0) {
      timeRemaining.value--;
    } else {
      submitQuiz();
    }
  }, 1000);
};

const selectAnswer = (option, index) => {
  if (!showResults.value) {
    selectedAnswers.value[index] = option;
  }
};

const submitQuiz = async () => {
  clearInterval(timer);
  showResults.value = true;

  // Calculate correct answers - backend uses correct_option (1,2,3,4) and option1,option2,etc.
  correctAnswers.value = quizQuestions.value.reduce(
    (count, question, index) => {
      const selectedAnswer = selectedAnswers.value[index];
      const correctOption = question.correct_option; // Backend returns 1,2,3,4

      // Convert selected answer (A,B,C,D) to number (1,2,3,4) for comparison
      const selectedOptionNumber =
        selectedAnswer === "A"
          ? 1
          : selectedAnswer === "B"
          ? 2
          : selectedAnswer === "C"
          ? 3
          : 4;

      return count + (selectedOptionNumber === correctOption ? 1 : 0);
    },
    0
  );

  // Submit score to backend
  try {
    const scoreData = {
      quizId: selectedQuiz.value.id,
      score: correctAnswers.value,
      totalQuestions: quizQuestions.value.length,
    };

    const response = await fetch("http://127.0.0.1:5006/api/submit-quiz", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${localStorage.getItem("token")}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify(scoreData),
    });

    if (response.ok) {
      // Immediately add the quiz to completed list to prevent retaking
      if (
        selectedQuiz.value &&
        !completedQuizzes.value.includes(selectedQuiz.value.id)
      ) {
        completedQuizzes.value.push(selectedQuiz.value.id);
      }
      console.log(
        "Quiz submitted successfully. Quiz ID:",
        selectedQuiz.value.id,
        "added to completed list"
      );
    } else {
      console.error("Failed to submit quiz score");
    }
  } catch (error) {
    console.error("Error submitting quiz score:", error);
  }
};

const finishQuiz = async () => {
  console.log(
    "Finishing quiz. Current completed quizzes:",
    completedQuizzes.value
  );

  // Add the completed quiz to the list if not already there
  if (
    selectedQuiz.value &&
    !completedQuizzes.value.includes(selectedQuiz.value.id)
  ) {
    completedQuizzes.value.push(selectedQuiz.value.id);
    console.log("Added quiz ID", selectedQuiz.value.id, "to completed list");
  }

  selectedQuiz.value = null;
  quizQuestions.value = [];
  selectedAnswers.value = {};
  currentQuestionIndex.value = 0;
  showResults.value = false;
  timeRemaining.value = 0;

  // Refresh quiz history from server to ensure consistency
  await fetchQuizHistory();

  console.log("Final completed quizzes list:", completedQuizzes.value);

  // Redirect to dashboard
  router.push("/");
};

const exitQuiz = () => {
  if (
    confirm(
      "Are you sure you want to exit the quiz? Your progress will be lost."
    )
  ) {
    clearInterval(timer);
    finishQuiz();
  }
};

// Computed properties for summary statistics
const totalTimeSpent = computed(() => {
  // Mock calculation - would come from actual quiz results
  return "2h 15m";
});

const averageScore = computed(() => {
  if (quizResults.value.length === 0) return 0;
  const total = quizResults.value.reduce(
    (sum, result) => sum + result.score_percentage,
    0
  );
  return Math.round(total / quizResults.value.length);
});

const bestScore = computed(() => {
  if (quizResults.value.length === 0) return 0;
  return Math.max(
    ...quizResults.value.map((result) => result.score_percentage)
  );
});

// Methods for quiz summary
const toggleQuizSummary = () => {
  showQuizSummary.value = !showQuizSummary.value;
  if (showQuizSummary.value) {
    loadQuizResults();
  }
};

const closeQuizSummary = () => {
  showQuizSummary.value = false;
};

const loadQuizResults = async () => {
  try {
    // Use mock data since the quiz-results endpoint doesn't exist yet
    quizResults.value = [
      {
        id: 1,
        quiz_title: "Mathematics Quiz 1",
        subject_name: "Mathematics",
        chapter_name: "Algebra",
        score_percentage: 85,
        correct_answers: 17,
        total_questions: 20,
        time_taken: "25m 30s",
        completed_at: "2024-01-15T10:30:00Z",
      },
      {
        id: 2,
        quiz_title: "Physics Quiz 2",
        subject_name: "Physics",
        chapter_name: "Mechanics",
        score_percentage: 92,
        correct_answers: 23,
        total_questions: 25,
        time_taken: "30m 15s",
        completed_at: "2024-01-14T14:20:00Z",
      },
      {
        id: 3,
        quiz_title: "Chemistry Quiz 1",
        subject_name: "Chemistry",
        chapter_name: "Organic Chemistry",
        score_percentage: 78,
        correct_answers: 15,
        total_questions: 20,
        time_taken: "22m 45s",
        completed_at: "2024-01-13T09:15:00Z",
      },
    ];
  } catch (error) {
    console.error("Error loading quiz results:", error);
  }
};

const getScoreBadgeClass = (score) => {
  if (score >= 90) return "badge excellent";
  if (score >= 80) return "badge good";
  if (score >= 70) return "badge average";
  return "badge poor";
};

const getTrendClass = (trend) => {
  if (trend > 0) return "trend-positive";
  if (trend < 0) return "trend-negative";
  return "trend-neutral";
};

// Methods for quiz filtering and organization
const setActiveFilter = (filter) => {
  activeFilter.value = filter;
};

const isExpired = (quiz) => {
  const now = new Date();
  const endDate = new Date(quiz.start_datetime);
  endDate.setHours(endDate.getHours() + quiz.duration_hours);
  endDate.setMinutes(endDate.getMinutes() + quiz.duration_minutes);
  return now > endDate;
};

const isUpcoming = (quiz) => {
  const now = new Date();
  const startDate = new Date(quiz.start_datetime);
  return now < startDate;
};

const getQuizStatusClass = (quiz) => {
  if (completedQuizzes.value.includes(quiz.id)) {
    return "status-completed";
  } else if (quiz.status === "expired") {
    return "status-expired";
  } else if (quiz.status === "upcoming") {
    return "status-upcoming";
  } else if (quiz.status === "active") {
    return "status-active";
  }
  return "status-inactive";
};

const getQuizStatusText = (quiz) => {
  if (completedQuizzes.value.includes(quiz.id)) {
    return "Completed";
  } else if (quiz.status === "expired") {
    return "Expired";
  } else if (quiz.status === "upcoming") {
    return "Upcoming";
  } else if (quiz.status === "active") {
    return "Active";
  }
  return "Inactive";
};

const getEmptyStateTitle = () => {
  switch (activeFilter.value) {
    case "active":
      return "No Active Quizzes";
    case "upcoming":
      return "No Upcoming Quizzes";
    case "expired":
      return "No Expired Quizzes";
    default:
      return "No Quizzes Found";
  }
};

const getEmptyStateMessage = () => {
  switch (activeFilter.value) {
    case "active":
      return "There are currently no active quizzes available. Check back later or try a different filter.";
    case "upcoming":
      return "No upcoming quizzes scheduled at the moment.";
    case "expired":
      return "No expired quizzes in your history.";
    default:
      return searchQuery.value
        ? "No quizzes match your search criteria."
        : "There are currently no quizzes available.";
  }
};

onMounted(() => {
  if (!localStorage.getItem("token")) {
    router.push("/login");
  }
  userFullName.value = localStorage.getItem("userFullName") || "Student";
  console.log("Component mounted, fetching data...");
  fetchData().then(() => {
    console.log("Data fetch completed. Quizzes count:", quizzes.value.length);
    console.log("Quizzes:", quizzes.value);
  });
});

onUnmounted(() => {
  if (timer) {
    clearInterval(timer);
  }
});

// Export all the reactive variables and functions
export {
  userFullName,
  quizzes,
  questions,
  chapters,
  subjects,
  selectedQuiz,
  quizQuestions,
  currentQuestionIndex,
  selectedAnswers,
  timeRemaining,
  quizDuration,
  showResults,
  correctAnswers,
  completedQuizzes,
  showQuizSummary,
  quizResults,
  performanceTrend,
  studyStreak,
  activeFilter,
  searchQuery,
  sortBy,
  filteredQuizzes,
  activeQuizzes,
  upcomingQuizzes,
  expiredQuizzes,
  currentQuestion,
  totalTimeSpent,
  averageScore,
  bestScore,
  logout,
  fetchData,
  fetchQuizHistory,
  getStatusBadge,
  getSubjectNameFromChapter,
  getChapterName,
  getDifficultyBadge,
  formatDate,
  formatTime,
  debugSelectQuiz,
  selectQuiz,
  startTimer,
  selectAnswer,
  submitQuiz,
  finishQuiz,
  exitQuiz,
  toggleQuizSummary,
  closeQuizSummary,
  loadQuizResults,
  getScoreBadgeClass,
  getTrendClass,
  setActiveFilter,
  isExpired,
  isUpcoming,
  getQuizStatusClass,
  getQuizStatusText,
  getEmptyStateTitle,
  getEmptyStateMessage,
  isSidebarCollapsed,
  toggleSidebar,
  isLoading,
};
