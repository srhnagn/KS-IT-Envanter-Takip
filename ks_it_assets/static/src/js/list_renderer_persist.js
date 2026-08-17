/** @odoo-module **/
import { ListRenderer } from "@web/views/list/list_renderer";
import { patch } from "@web/core/utils/patch";
import { browser } from "@web/core/browser/browser";

const STORAGE_KEY = "ks_list_widths";

patch(ListRenderer.prototype, {
    freezeColumnWidths() {
        super.freezeColumnWidths();
        
        const resModel = this.props.list && this.props.list.resModel;
        if (!resModel) return;

        const key = `${STORAGE_KEY}_${resModel}`;
        const saved = browser.localStorage.getItem(key);
        
        if (saved) {
            try {
                const parsed = JSON.parse(saved);
                const table = this.tableRef.el;
                if (!table) return;

                let applied = false;
                const headers = [...table.querySelectorAll("thead th:not(.o_list_actions_header)")];
                headers.forEach((th, index) => {
                    const fieldName = th.dataset.name;
                    if (fieldName && parsed[fieldName]) {
                        const w = parsed[fieldName];
                        th.style.width = `${w}px`;
                        th.style.maxWidth = `${w}px`;
                        if (this.columnWidths) {
                            this.columnWidths[index] = w;
                        }
                        applied = true;
                    }
                });
                
                if (applied) {
                    this.keepColumnWidths = true;
                }
            } catch (e) {
                console.warn("Failed to restore KS column widths", e);
            }
        }
    },

    onStartResize(ev) {
        super.onStartResize(ev);
        const resModel = this.props.list && this.props.list.resModel;
        if (!resModel) return;

        const key = `${STORAGE_KEY}_${resModel}`;
        const saveWidths = () => {
            const table = this.tableRef.el;
            if (!table) return;
            const headers = [...table.querySelectorAll("thead th:not(.o_list_actions_header)")];
            
            let widthsToSave = {};
            const saved = browser.localStorage.getItem(key);
            if (saved) {
                try { widthsToSave = JSON.parse(saved); } catch (e) {}
            }

            headers.forEach(th => {
                const fieldName = th.dataset.name;
                if (fieldName && th.style.width) {
                    widthsToSave[fieldName] = parseFloat(th.style.width);
                }
            });
            browser.localStorage.setItem(key, JSON.stringify(widthsToSave));
            window.removeEventListener("pointerup", saveWidths);
        };
        window.addEventListener("pointerup", saveWidths);
    }
});
