/* Copyright 2020 Karlsruhe Institute of Technology
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License. */

import CanvasPainter from 'scripts/lib/components/CanvasPainter.vue';
import UploadManager from 'scripts/lib/components/UploadManager.vue';
import WorkflowEditor from 'scripts/lib/components/WorkflowEditor.vue';

new Vue({
  el: '#vm',
  components: {
    CanvasPainter,
    UploadManager,
    WorkflowEditor,
  },
  data: {
    currentTab: null,
    drawing: {
      origin: 'drawing',
      filename: '',
      currentFile: null,
      currentFileUrl: null,
      unsavedChanges: false,
      uploading: false,
    },
    workflow: {
      origin: 'workflow',
      filename: '',
      currentFile: null,
      currentFileUrl: null,
      unsavedChanges: false,
      uploading: false,
    },
  },
  methods: {
    changeTab(tab) {
      this.currentTab = tab;
    },
    updateUrl(file) {
      // Update the current (or last uploaded) file in the URL as well.
      const url = kadi.utils.setSearchParam('file', file.id);
      kadi.utils.replaceState(url);
    },
    updateUploadState(origin) {
      if (origin === this.drawing.origin) {
        this.drawing.uploading = false;
      } else if (origin === this.workflow.origin) {
        this.workflow.uploading = false;
      }
    },
    uploadCompleted(file, origin) {
      if (origin === this.drawing.origin) {
        this.drawing.currentFile = file;
        this.updateUrl(file);
        kadi.alert($t('Drawing uploaded successfully.'), {type: 'success', scrollTo: false});
      } else if (origin === this.workflow.origin) {
        this.workflow.currentFile = file;
        this.updateUrl(file);
        kadi.alert($t('Workflow uploaded successfully.'), {type: 'success', scrollTo: false});
      }

      this.updateUploadState(origin);
    },
    uploadCanceled(upload, origin) {
      this.updateUploadState(origin);
    },
    uploadFile(currentFile, file, origin) {
      // When trying to replace a file that is currently being edited, we skip the confirmation for replacing existing
      // files.
      this.$refs.uploadManager.addFile(file, currentFile && currentFile.name === file.name, origin);
    },
    checkFile(currentFile, filename, callback) {
      if (currentFile && currentFile.name === filename) {
        axios.get(currentFile._links.self)
          .then((response) => {
            // Check if the content of the current file has changed since loading or last uploading it by just comparing
            // the checksums.
            if (currentFile.checksum !== response.data.checksum) {
              let warningMsg = $t('The content of the file you are currently editing changed since loading it.');
              warningMsg += `\n${$t('Do you still want to overwrite it?')}`;

              if (window.confirm(warningMsg)) {
                callback();
              }
            } else {
              callback();
            }
          });
      } else {
        callback();
      }
    },
    dataURLtoFile(dataurl, filename) {
      const bstr = window.atob(dataurl.split(',')[1]);
      let n = bstr.length;
      const u8arr = new Uint8Array(n);

      while (n) {
        u8arr[n - 1] = bstr.charCodeAt(n - 1);
        n -= 1;
      }
      return new File([u8arr], filename);
    },
    saveDrawing(canvas) {
      let filename = this.drawing.filename;
      if (!filename.endsWith('.png')) {
        filename += '.png';
      }

      const _uploadImage = () => {
        const file = this.dataURLtoFile(canvas.toDataURL(), filename);
        this.uploadFile(this.drawing.currentFile, file, this.drawing.origin);
        this.drawing.uploading = true;
        this.drawing.unsavedChanges = false;
      };

      this.checkFile(this.drawing.currentFile, filename, _uploadImage);
    },
    saveWorkflow(editor) {
      let filename = this.workflow.filename;
      if (!filename.endsWith('.flow')) {
        filename += '.flow';
      }

      const _uploadWorkflow = () => {
        const file = new File([JSON.stringify(editor.toFlow())], filename);
        this.uploadFile(this.workflow.currentFile, file, this.workflow.origin);
        this.workflow.uploading = true;
        this.workflow.unsavedChanges = false;
      };

      this.checkFile(this.workflow.currentFile, filename, _uploadWorkflow);
    },
  },
  mounted() {
    if (kadi.js_resources.current_file_endpoint) {
      axios.get(kadi.js_resources.current_file_endpoint)
        .then((response) => {
          const data = response.data;
          let uploadType = null;

          if (['image/jpeg', 'image/png'].includes(data.magic_mimetype)) {
            uploadType = 'drawing';
          } else if (data.magic_mimetype === 'application/x-flow+json') {
            uploadType = 'workflow';
          }

          if (uploadType !== null) {
            this[uploadType].currentFile = data;
            this[uploadType].currentFileUrl = data._links.download;
            this[uploadType].filename = data.name;

            this.$refs.navTabs.changeTab(uploadType);
          }
        })
        .catch((error) => kadi.alert($t('Error loading file.'), {request: error.request}));
    }
  },
});
