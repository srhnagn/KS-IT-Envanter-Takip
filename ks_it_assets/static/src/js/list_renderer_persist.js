/** @odoo-module **/
import { ListRenderer } from "@web/views/list/list_renderer";
import { patch } from "@web/core/utils/patch";
import { browser } from "@web/core/browser/browser";

const STORAGE_KEY = "ks_list_widths";

patch(ListRenderer.prototype, {
    setup() {
        super.setup();
        this.ksRestoredWidths = false;
    },

    freezeColumnWidths() {
        const resModel = this.props.list && this.props.list.resModel;
        
        if (resModel && !this.keepColumnWidths) {
            const key = `${STORAGE_KEY}_${resModel}`;
            const saved = browser.localStorage.getItem(key);
            
            if (saved) {
                try {
                    const parsed = JSON.parse(saved);
                    const table = this.tableRef.el;
                    if (table) {
                        const headers = [...table.querySelectorAll("thead th:not(.o_list_actions_header)")];
                        
                        // We must compute first to get default/content widths for columns we haven't manually resized
                        // But we need to briefly un-fix table layout to let Odoo compute natural widths
                        table.style.tableLayout = "auto";
                        table.style.width = null;
                        headers.forEach((th) => {
                            th.style.width = null;
                            th.style.maxWidth = null;
                        });
                        const computed = this.computeColumnWidthsFromContent();
                        table.style.tableLayout = "fixed";

                        // Now merge saved widths with computed widths
                        this.columnWidths = headers.map((th, index) => {
                            const fieldName = th.dataset.name;
                            return (fieldName && parsed[fieldName]) ? parsed[fieldName] : computed[index];
                        });

                        this.keepColumnWidths = true;
                        this.ksRestoredWidths = true;
                    }
                } catch (e) {
                    console.warn("Failed to restore KS column widths", e);
                }
            }
        }
        
        super.freezeColumnWidths();
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
            
            // Get existing saved widths to not overwrite un-rendered optional columns
            let widthsToSave = {};
            const saved = browser.localStorage.getItem(key);
            if (saved) {
                try { widthsToSave = JSON.parse(saved); } catch (e) {}
            }

            headers.forEach(th => {
                const fieldName = th.dataset.name;
                // If it has inline style width from resize, save it
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
