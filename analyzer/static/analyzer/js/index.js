function handleImageChange(event) {
    const file = event.target.files[0];
    if (!file) return;

    const preview = document.getElementById("preview");
    preview.src = URL.createObjectURL(file);

    // Khởi tạo metadata với các thông tin cơ bản
    const metadata = {
        fileName: file.name,
        fileSizeKB: +(file.size / 1024).toFixed(2),  // số thôi, không kèm "KB"
        mimeType: file.type,
        fileExtension: file.name.split('.').pop().toLowerCase(),
        lastModified: new Date(file.lastModified).toISOString(), // chuẩn ISO
        isRaster: isRaster(file.type),
        canPreview: file.type.startsWith("image/"),
        width: null,
        height: null,
        aspectRatio: null,
        orientation: null,
        estimatedDpi: null
    };

    const reader = new FileReader();
    reader.onload = function(e) {
        const img = new Image();
        img.onload = function() {
            metadata.width = img.width;
            metadata.height = img.height;
            metadata.aspectRatio = +(img.width / img.height).toFixed(2);
            metadata.orientation = img.width > img.height ? "landscape" : (img.width < img.height ? "portrait" : "square");
            metadata.estimatedDpi = Math.round(img.width / 8); // giả định ảnh rộng 8 inch

            // Cập nhật lại input hidden chứa metadata JSON sau khi ảnh load xong
            const hiddenMeta = document.getElementById("image_metadata");
            if (hiddenMeta) hiddenMeta.value = JSON.stringify(metadata);
        };
        img.src = e.target.result;
    };
    reader.readAsDataURL(file);

    // Gán tạm thời metadata cơ bản (chưa có kích thước ảnh)
    const hiddenMeta = document.getElementById("image_metadata");
    if (hiddenMeta) hiddenMeta.value = JSON.stringify(metadata);
}

function isRaster(mimeType) {
    const rasterTypes = ["image/png", "image/jpeg", "image/jpg", "image/gif", "image/bmp", "image/webp"];
    return rasterTypes.includes(mimeType.toLowerCase());
}
