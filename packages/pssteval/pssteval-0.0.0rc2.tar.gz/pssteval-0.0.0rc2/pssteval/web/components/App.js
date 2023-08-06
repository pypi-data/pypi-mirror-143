import AlignedSteps from "./AlignedSteps.js";
import Details from "./Details.js";
import TranscriptFormatted from "./TranscriptFormatted.js";
import AudioPlayer from "./AudioPlayer.js";

export default {
        components: { AlignedSteps, Details, TranscriptFormatted, AudioPlayer },
        data() {
            return {
                analysisFiles: [],
                utterances: null,
                details: null,
                detailHoverIndex: null,
                nFeatures: 24,
                overallFer: null,
                overallPer: null,
                alphabet: "arpabet",
            }
        },
        methods: {
            sum(arr) {
                return arr.reduce((partialSum, a) => partialSum + a, 0);
            },
            errorRate(utterances, selector) {
                if (!utterances) {
                    return null;
                }
                let totalLength = this.sum(Array.from(utterances.entries()).map(([id, u]) => selector(u).expected_length));
                let errors = this.sum(Array.from(utterances.entries()).map(([id, u]) => selector(u).distance));
                return errors / totalLength
            },
            fer(utterances) {
                return `${(100 * this.errorRate(utterances, u => u.features)).toFixed(1)}%`;
            },
            per(utterances) {
                return `${(100 * this.errorRate(utterances, u => u.phonemes)).toFixed(1)}%`;
            },

            updateUtterances(utterances) {
                let sorted = this.sortUtterances(utterances);
                this.utterances = sorted;
                let detail_id = Array.from(sorted.keys())[0];
                this.setDetails(detail_id, utterances[detail_id]);
            },
            setDetails(utteranceId, utterance) {
                this.details = { utterance_id: utteranceId, utterance: utterance };
            },
            sortUtterances(utterances) {
                return new Map([...Object.entries(utterances)
                    .map(([id, value]) => [id, value])
                    .sort((l, r) => r[1].features.error_rate - l[1].features.error_rate)
                ]);
            },
            costFormatted(cost) {
                let rounded = Math.round(100 * this.nFeatures * cost, 2) / 100
                return `${rounded}`
            },
            utteranceFeatureCost(utterance) {
                return `${this.costFormatted(utterance.features.distance)} / ${utterance.features.expected_length * this.nFeatures}`
            },
            utterancePhonemeCost(utterance) {
                return `${utterance.phonemes.distance} / ${utterance.phonemes.expected_length}`
            },
            transcriptExpected(utterance) {
                return utterance.features.steps.map(s => s.expected).filter(t => t);
            },
            transcriptActual(utterance) {
                return utterance.features.steps.map(s => s.actual).filter(t => t);
            },
        },
        async created () {
            this.analysisFiles = await fetch("./analysis-files").then(r => r.json());
            await fetch(this.analysisFiles[0]).then(r => r.json()).then(this.updateUtterances);
        },
    template: `
        <div id="results">
        <div id="top-pane">
            <h1>
                PSST Error Analysis
            </h1>
            <div id="alphabet-picker">
                <input type="radio" name="alphabet" id="radio-ipa" value="ipa" v-model="alphabet" />
                <label for="radio-ipa">IPA</label>
                <input type="radio" name="alphabet" id="radio-arpabet" value="arpabet" v-model="alphabet" />
                <label for="radio-arpabet">ARPAbet</label>
            </div>
            <table>
                <thead>
                    <tr>
                        <td>Overall FER</td>
                        <td>Overall PER</td>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>{{fer(utterances)}}</td>
                        <td>{{per(utterances)}}</td>
                    </tr>
                </tbody>
            </table>

        </div>
        <div id="result-table-wrapper">
            <table id="result-table">
                <thead>
                    <tr class="header-extra">
                        <th>&nbsp;</th>
                        <th>&nbsp;</th>
                        <th>&nbsp;</th>
                        <th colspan="2" class="header-features" >Features</th>
                        <th colspan="2" class="header-phonemes" >Phonemes</th>
                    </tr>

                    <tr class="header-main">
                        <th>Utterance ID</th>
                        <th>Transcript (True/Predicted)</th>
                        <th>FER</th>
                        <th>Err/Len</th>
                        <th>PER</th>
                        <th>Err/Len</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="[utteranceId, utterance] in utterances" :class="{highlight: utterance == details.utterance}">
                        <td>
                            <button @click="setDetails(utteranceId, utterance)">{{utteranceId}}</button>
                        </td>
                        <td class="transcript">
                            <AlignedSteps :steps="utterance.features.steps" :alphabet="alphabet" />
                        </td>
                        <td class="align-right">
                            {{(utterance.features.error_rate * 100).toFixed(1)}}%
                        </td>
                        <td class="align-right">
                            {{ utteranceFeatureCost(utterance) }}
                        </td>
                        <td class="align-right">
                            {{(utterance.phonemes.error_rate * 100).toFixed(1)}}%
                        </td>
                        <td class="align-right">
                            {{ utterancePhonemeCost(utterance) }}
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>

        <div id="item" v-if="!!details">
            <h2>{{details.utterance_id}}</h2>
            <div>
                <AlignedSteps :steps="details.utterance.features.steps" :alphabet="alphabet" :detailHoverIndex="detailHoverIndex "/>
            </div>
            <table id="details-error-rates">
                <thead>
                    <tr>
                        <td>Utterance FER</td>
                        <td>Utterance PER</td>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>{{(100 * details.utterance.features.error_rate).toFixed(1)}}%</td>
                        <td>{{(100 * details.utterance.phonemes.error_rate).toFixed(1)}}%</td>
                    </tr>
                </tbody>
            </table>
            <AudioPlayer :utteranceId="details.utterance_id" />
        </div>

        <Details 
            v-if="!!details" :steps="details.utterance.features.steps"
            :alphabet="alphabet"
            :detailHoverIndex="detailHoverIndex"
            :nFeatures="nFeatures"/>
    </div>`
};