// ��ҳ�Ķ�̬Ч��
window.addEventListener('load', function () {
    gsap.from(".title", { duration: 1, y: -100, opacity: 0, ease: "bounce.out" });
    gsap.from(".description", { duration: 1, opacity: 0, y: 50, stagger: 0.3 });
});

// ����ҳ�� - ��̬���ز�������
document.addEventListener('DOMContentLoaded', function () {
    const blogList = document.getElementById('blog-list');

    // ��ȡdataĿ¼�е�md�ļ�
    fetch('/data')
        .then(response => response.json())
        .then(files => {
            files.forEach(file => {
                const blogItem = document.createElement('div');
                blogItem.classList.add('blog-item');
                blogItem.innerHTML = file.title;  // �����ļ���������
                blogItem.onclick = function() {
                    loadBlogContent(file.name);
                };
                blogList.appendChild(blogItem);
            });
        })
        .catch(err => console.error(err));

    // ���ز�������
    function loadBlogContent(filename) {
        fetch(`/data/${filename}`)
            .then(response => response.text())
            .then(mdContent => {
                const htmlContent = marked.parse(mdContent);
                const blogPost = document.createElement('div');
                blogPost.classList.add('section');
                blogPost.innerHTML = htmlContent;
                document.body.appendChild(blogPost);
            });
    }
});
