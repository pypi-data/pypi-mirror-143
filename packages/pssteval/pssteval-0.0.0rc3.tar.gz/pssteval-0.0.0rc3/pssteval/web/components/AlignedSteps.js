import TranscriptFormatted from "./TranscriptFormatted.js";

export default {
    props: ["steps", "alphabet", "detailHoverIndex"],
    components: {TranscriptFormatted},
    template: `
        <div class="transcript-steps-wrapper">
          <div class="transcript-steps">
             <div class="transcript-step"
                :class="['action-'+step.action.toLowerCase()]"
                 v-for="step, n in steps">
                 
                <div class="expected" :class="{ highlight: detailHoverIndex == n }">
                    <TranscriptFormatted :transcript="step.expected" :alphabet="alphabet" />
                </div>
                <div class="actual" :class="{ highlight: detailHoverIndex == n }">
                    <TranscriptFormatted :transcript="step.actual" :alphabet="alphabet" />
                </div>
            </div>
          </div>
        </div>`
};