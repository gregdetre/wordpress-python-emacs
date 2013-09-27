(defun wordpress-save-this-file (&optional post-status)
  (interactive)
  (save-buffer)
  (let* ((filen (buffer-file-name))
         (post-status-str (if post-status
                              (concat "--post-status " post-status)
                            ""))
         ;; you may need to hardcode this to point to create_update_post.py
         (cmd (format "python create_update_post.py -f '%s' %s" filen post-status-str)))
      (message cmd)
      (shell-command cmd)
      ))

(defun wordpress-publish-this-file ()
  (interactive)
  (wordpress-save-this-file "publish"))
