function get_total_likes(post_id) {
    fetch(`/likes/${post_id}`)
    .then(response => response.json())
    .then(data => {
        likes = document.querySelector(`#post-${post_id}-likes`);

        if(!data.liked) {
            likes.innerHTML = `<button class="like-btn" onclick=toggle_like(${post_id})><i class="bi bi-heart"></i></button> ${data.total_likes}`;
        }
        else {
            likes.innerHTML = `<button class="like-btn" onclick=toggle_like(${post_id})><i class="bi bi-heart-fill"></i></button> ${data.total_likes}`;
        }
    });
}

function toggle_like(post_id) {
    fetch(`/likes/${post_id}`)
    .then(response => response.json())
    .then(data => {
        //add like if not already liked
        if(!data.liked) {
            fetch('/likes', {
                method: 'POST',
                body: JSON.stringify({
                    post_id: post_id
                })
            })
            //allow time to update db
            setTimeout(() => {
                fetch(`/likes/${post_id}`)
                .then(response => response.json())
                .then(data => {
                    //change heart to filled heart
                    //show new like count ++
                    const p = document.querySelectorAll(`#post-${post_id} p`);
                    p[3].innerHTML = `<button class="like-btn" onclick=toggle_like(${post_id})><i class="bi bi-heart-fill"></i></button> ${data.total_likes}`;
                });
            }, 100);
        }
        //remove like if previously liked
        else {
            fetch('/likes', {
                method: 'PUT',
                body: JSON.stringify({
                    post_id: post_id
                })
            })
            //allow time to update db
            setTimeout(() => {
                fetch(`/likes/${post_id}`)
                .then(response => response.json())
                .then(data => {
                    //change filled heart to outlined heart
                    //show new like count, count--
                    const p = document.querySelectorAll(`#post-${post_id} p`);
                    p[3].innerHTML = `<button class="like-btn" onclick=toggle_like(${post_id})><i class="bi bi-heart"></i></button> ${data.total_likes}`;
                });
            }, 100);
        }
    });
}

function edit_post(post_id) {
    //get data to prefill textarea
    fetch(`/posts/${post_id}`)
    .then(response => response.json())
    .then(post => {
        //create textarea to allow editing post
        const textarea = document.createElement('textarea');
        textarea.innerHTML = post.content; //set textarea content to existing post content

        //replace p tag with editable textarea tag
        const p = document.querySelectorAll(`#post-${post_id} p`);
        p[1].replaceWith(textarea);

        //create done button and replace with edit button
        const edit_btn = document.querySelector(`#post-${post_id} button`);
        const done_btn = document.createElement('button');
        done_btn.innerHTML = 'Done';
        done_btn.classList.add('done-btn');
        edit_btn.replaceWith(done_btn);

        //submitting edited text
        done_btn.addEventListener('click', function() {
            done_editing(post.id, textarea, p, edit_btn, done_btn);
        });
    });
}

function done_editing(post_id, textarea, p, edit_btn, done_btn) {
    //update post's content in db
    fetch(`/posts/${post_id}`, {
        method: 'PUT',
        body: JSON.stringify({
            post_id: post_id,
            new_content: textarea.value
        })
    });
    //allow time to update db
    setTimeout(() => {
        //fetch updated content to show user
        fetch(`/posts/${post_id}`)
        .then(response => response.json())
        .then(post => {
            //remove created textarea and button
            p[1].innerHTML = post.content;
            textarea.replaceWith(p[1]);
            done_btn.replaceWith(edit_btn);
        });
    }, 100);
}
