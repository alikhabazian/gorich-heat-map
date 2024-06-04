var series = [];
var value = 0;

window.addEventListener("DOMContentLoaded", () => {
  

    // ##############################################################################
    // ####################################### elements defenition
    //##############################################################################
    
    // ##############################################################################
    // ####################################### variables defenition
    //##############################################################################

    let getSequencesUrl = "http://localhost:9090/signal/getSequences";
    let saveDatasetsUrl = "http://localhost:9090/signal/saveDatasets";
    let is_paused = false;
  

    // ##############################################################################
    // ####################################### buttons event handling
    //##############################################################################



    // ##############################################################################
    // ####################################### functions
    //##############################################################################
    function addDatasetLoading(loading) {
      if (loading) {
        btnAddDataset.setAttribute("disabled", "disabled");
        btnAddDatasetLoading.classList.remove("visually-hidden");
      } else {
        btnAddDataset.removeAttribute("disabled");
        btnAddDatasetLoading.classList.add("visually-hidden");
      }
    }

    function saveDatasetLoading(loading) {
      if (loading) {
        btnSaveDataset.setAttribute("disabled", "disabled");
        btnSaveDatasetLoading.classList.remove("visually-hidden");
      } else {
        btnSaveDataset.removeAttribute("disabled");
        btnSaveDatasetLoading.classList.add("visually-hidden");
      }
    }

    function clearAxisRanges() {
      axisRangesLen = xAxis.axisRanges._values.length;
      for (let i = 0; i < axisRangesLen; ++i) {
        // xAxis.axisRanges.getIndex(i).dispose();
        xAxis.axisRanges.removeValue(xAxis.axisRanges.getIndex(0));
      }
    }


});