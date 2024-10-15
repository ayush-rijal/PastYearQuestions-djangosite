document.addEventListener("DOMContentLoaded", function () {
  const commentForm = document.getElementById("comment-form");
  const commentsContainer = document.getElementById("comments-container");
  const commentContent = document.getElementById("comment-content");
  const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;

  commentForm.addEventListener("submit", function (e) {
    e.preventDefault();
    const content = commentContent.value;
    if (content.trim()) {
      submitComment(content);
    }
  });

  commentsContainer.addEventListener("click", function (e) {
    if (e.target.classList.contains("like-button")) {
      const commentId = e.target.closest("[data-comment-id]").dataset.commentId;
      likeComment(commentId);
    } else if (e.target.classList.contains("reply-button")) {
      const commentElement = e.target.closest("[data-comment-id]");
      scrollToCommentSection();
      focusCommentInput(`@${commentElement.dataset.username} `);
    }
  });

  function submitComment(content, parentId = null) {
    const url = parentId
      ? `/post/${postId}/comment/?parent_id=${parentId}`
      : `/post/${postId}/comment/`;

    fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
        "X-CSRFToken": csrfToken,
      },
      body: `content=${encodeURIComponent(content)}`,
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.status === "success") {
          addCommentToDOM(data, parentId);
          commentContent.value = "";
        }
      });
  }

  function likeComment(commentId) {
    fetch(`/comment/${commentId}/like/`, {
      method: "POST",
      headers: {
        "X-CSRFToken": csrfToken,
      },
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.status === "success") {
          updateLikeCount(commentId, data.likes);
        }
      });
  }

  function scrollToCommentSection() {
    commentForm.scrollIntoView({ behavior: "smooth", block: "start" });
  }

  function focusCommentInput(prefill = "") {
    commentContent.value = prefill;
    commentContent.focus();
    commentContent.setSelectionRange(
      commentContent.value.length,
      commentContent.value.length
    );
  }

  function addCommentToDOM(comment, parentId) {
    const commentHTML = `
            <div class="bg-gray-100 p-4 rounded-lg mt-4" data-comment-id="${comment.id}" data-username="${comment.user}">
                <div class="flex items-center space-x-2 mb-2">
                    <div class="w-8 h-8 rounded-full bg-gray-300"></div>
                    <span class="font-semibold">${comment.user}</span>
                    <span class="text-sm text-gray-500">${comment.created_at}</span>
                </div>
                <p class="mb-2">${comment.content}</p>
                <div class="flex items-center space-x-2">
                    <button class="like-button text-sm text-gray-500 hover:text-blue-500">Like (0)</button>
                    <button class="reply-button text-sm text-gray-500 hover:text-blue-500">Reply</button>
                </div>
            </div>
        `;
    if (parentId) {
      const parentComment = document.querySelector(
        `[data-comment-id="${parentId}"]`
      );
      let repliesContainer = parentComment.querySelector(".replies");
      if (!repliesContainer) {
        repliesContainer = document.createElement("div");
        repliesContainer.className = "replies mt-4 ml-8";
        parentComment.appendChild(repliesContainer);
      }
      repliesContainer.insertAdjacentHTML("beforeend", commentHTML);
    } else {
      commentsContainer.insertAdjacentHTML("afterbegin", commentHTML);
    }
  }

  function updateLikeCount(commentId, likes) {
    const likeButton = document.querySelector(
      `[data-comment-id="${commentId}"] .like-button`
    );
    likeButton.textContent = `Like (${likes})`;
  }
});
