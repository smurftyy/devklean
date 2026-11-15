import React, { useState } from 'react';
import { Minus, Plus } from 'lucide-react';
import { FAQ_ITEMS } from '../data';

export default function FaqSection() {
  const [openId, setOpenId] = useState<string | null>(FAQ_ITEMS[0].id);

  const toggle = (id: string) => {
    setOpenId((prev) => (prev === id ? null : id));
  };

  return (
    <section id="faq" className="w-full scroll-mt-16 border-b border-[#333333] bg-[#111111] py-14 md:py-20">
      <div className="mx-auto max-w-[1200px] px-5 md:px-6 lg:px-8">
        <div className="grid gap-10 lg:grid-cols-12 lg:gap-12">
          <div className="lg:col-span-4">
            <h2 className="font-sans text-[32px] font-medium leading-[1.1] tracking-[-0.025em] text-[#F5F5F5] md:text-[42px]">
              Frequently asked.
            </h2>
          </div>

          <div className="border-t border-[#333333] lg:col-span-8">
            {FAQ_ITEMS.map((item) => {
              const isOpen = openId === item.id;
              return (
                <div key={item.id} className="border-b border-[#333333]">
                  <button
                    type="button"
                    onClick={() => toggle(item.id)}
                    aria-expanded={isOpen}
                    aria-controls={`faq-answer-${item.id}`}
                    className="flex min-h-[58px] w-full items-center justify-between gap-4 py-4 text-left transition-colors hover:text-[#F5F5F5]"
                  >
                    <span className="font-sans text-[16px] font-medium text-[#F5F5F5] md:text-[17px]">
                      {item.question}
                    </span>
                    <span className="inline-flex h-6 w-6 shrink-0 items-center justify-center text-[#ADADAD]">
                      {isOpen ? (
                        <Minus className="h-4 w-4" strokeWidth={1.6} aria-hidden="true" />
                      ) : (
                        <Plus className="h-4 w-4" strokeWidth={1.6} aria-hidden="true" />
                      )}
                    </span>
                  </button>

                  {isOpen && (
                    <div id={`faq-answer-${item.id}`} className="pb-6 pr-8">
                      <p className="max-w-[64ch] font-sans text-[15px] leading-[1.65] text-[#ADADAD]">
                        {item.answer}
                      </p>
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        </div>
      </div>
    </section>
  );
}
