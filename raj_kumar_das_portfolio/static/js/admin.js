/* ==========================================================================
   Raj Kumar Das Portfolio - Admin Inbox & Dashboard JS
   ========================================================================== */

document.addEventListener('DOMContentLoaded', () => {

  // --- MESSAGE DETAIL MODAL & ACTIONS ---
  const messageModalElement = document.getElementById('messageDetailModal');
  const messageModal = messageModalElement ? new bootstrap.Modal(messageModalElement) : null;
  const deleteConfirmModalElement = document.getElementById('deleteConfirmModal');
  const deleteConfirmModal = deleteConfirmModalElement ? new bootstrap.Modal(deleteConfirmModalElement) : null;

  let activeMessageId = null;

  // View Message Detail
  document.querySelectorAll('.btn-view-msg').forEach(btn => {
    btn.addEventListener('click', () => {
      const msgId = btn.getAttribute('data-id');
      const name = btn.getAttribute('data-name');
      const email = btn.getAttribute('data-email');
      const subject = btn.getAttribute('data-subject');
      const date = btn.getAttribute('data-date');
      const message = btn.getAttribute('data-message');
      const status = btn.getAttribute('data-status');

      activeMessageId = msgId;

      document.getElementById('modalMsgId').textContent = `#${msgId}`;
      document.getElementById('modalSenderName').textContent = name;
      document.getElementById('modalSenderEmail').textContent = email;
      document.getElementById('modalSenderEmail').href = `mailto:${email}`;
      document.getElementById('modalSubject').textContent = subject;
      document.getElementById('modalDate').textContent = date;
      document.getElementById('modalMessageBody').textContent = message;
      document.getElementById('modalStatusBadge').textContent = status;

      // Update badge class
      const badge = document.getElementById('modalStatusBadge');
      badge.className = 'badge ' + (status === 'Unread' ? 'badge-unread' : (status === 'Read' ? 'badge-read' : 'badge-replied'));

      // Setup Reply Mailto link
      const replyBtn = document.getElementById('modalReplyBtn');
      if (replyBtn) {
        replyBtn.href = `mailto:${email}?subject=Re: ${encodeURIComponent(subject)}&body=${encodeURIComponent('\n\n--- Original Message ---\nFrom: ' + name + '\nSubject: ' + subject + '\n' + message)}`;
      }

      if (messageModal) {
        messageModal.show();
      }

      // Automatically mark unread message as read when viewed
      if (status === 'Unread') {
        updateMessageStatus(msgId, 'Read', false);
      }
    });
  });

  // Toggle Read / Unread Status Button Handlers
  document.querySelectorAll('.btn-toggle-status').forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.stopPropagation();
      const msgId = btn.getAttribute('data-id');
      const targetStatus = btn.getAttribute('data-target-status');
      updateMessageStatus(msgId, targetStatus, true);
    });
  });

  // Toggle status from inside detail modal
  const markReadModalBtn = document.getElementById('modalMarkReadBtn');
  const markUnreadModalBtn = document.getElementById('modalMarkUnreadBtn');

  if (markReadModalBtn) {
    markReadModalBtn.addEventListener('click', () => {
      if (activeMessageId) updateMessageStatus(activeMessageId, 'Read', true);
    });
  }

  if (markUnreadModalBtn) {
    markUnreadModalBtn.addEventListener('click', () => {
      if (activeMessageId) updateMessageStatus(activeMessageId, 'Unread', true);
    });
  }

  // Delete Confirmation Trigger
  document.querySelectorAll('.btn-delete-msg').forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.stopPropagation();
      activeMessageId = btn.getAttribute('data-id');
      if (deleteConfirmModal) {
        deleteConfirmModal.show();
      }
    });
  });

  const modalDeleteBtn = document.getElementById('modalDeleteBtn');
  if (modalDeleteBtn) {
    modalDeleteBtn.addEventListener('click', () => {
      if (activeMessageId) {
        if (messageModal) messageModal.hide();
        deleteMessage(activeMessageId);
      }
    });
  }

  const confirmDeleteActionBtn = document.getElementById('confirmDeleteActionBtn');
  if (confirmDeleteActionBtn) {
    confirmDeleteActionBtn.addEventListener('click', () => {
      if (activeMessageId) {
        deleteMessage(activeMessageId);
      }
    });
  }

  // AJAX Status Update Handler
  async function updateMessageStatus(msgId, newStatus, reloadPage = true) {
    try {
      const response = await fetch(`/admin/api/messages/${msgId}/status`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ status: newStatus })
      });

      const data = await response.json();
      if (response.ok && data.success) {
        if (reloadPage) {
          window.location.reload();
        }
      } else {
        alert(data.message || 'Failed to update message status.');
      }
    } catch (err) {
      console.error('Error updating status:', err);
    }
  }

  // AJAX Delete Message Handler
  async function deleteMessage(msgId) {
    try {
      const response = await fetch(`/admin/api/messages/${msgId}/delete`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
      });

      const data = await response.json();
      if (response.ok && data.success) {
        if (deleteConfirmModal) deleteConfirmModal.hide();
        window.location.reload();
      } else {
        alert(data.message || 'Failed to delete message.');
      }
    } catch (err) {
      console.error('Error deleting message:', err);
    }
  }

});
